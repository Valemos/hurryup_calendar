import enum
from abc import ABC
from datetime import datetime
import psycopg2
import psycopg2.sql as sql

from application.event import Event, EventParticipants
from application.event_group import EventGroup
from application.event_parametric import EventParametric
from application.event_pattern import EventPattern
from application.user import User
from database.database_savable import DatabaseSavable


class DatabaseHandler:
    # dictionary for table columns   table_name : [table columns]
    _tables_list = [User, EventGroup, Event, EventPattern, EventParametric, EventParticipants]

    def __init__(self,
                 new_name="CalendarApp",
                 new_pass="1",
                 new_port="5432",
                 new_host="localhost",
                 new_user="postgres"):

        # values to connect to DB
        self._name_db = new_name
        self._pass_db = new_pass
        self._port_db = new_port
        self._host_db = new_host
        self._user_db = new_user
        self._main_connection = None

        # check connection to database
        self._connected_db = self._try_connect_db()

        # debug
        # if self._connected_db:
        #     print("Connected successfully")
        # else:
        #     print("Connection failed")

        # self._recreate_all_tables() # DELETE current tables and create new tables

    def __del__(self):
        """Close connection on delete"""
        if self._main_connection is not None:
            self._main_connection.close()

    def _try_connect_db(self):  # connecting to DB
        """Creates connection to database with necessary credentials and initializes cursor"""

        try:
            self._main_connection = psycopg2.connect(
                dbname=self._name_db,
                user=self._user_db,
                password=self._pass_db,
                host=self._host_db,
                port=self._port_db)

            self._main_cursor = self._main_connection.cursor()
            return True
        except Exception as exc:
            print(f"connection to database failed {exc}")
            return False

    def check_connected(self):
        """Returns True if connection established, else returns False."""
        return self._connected_db

    def _correct_tables(self):
        """check Tables and create it if not exists"""

        # check every table and create if not exists
        for table in DatabaseHandler._tables_list:
            self._main_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table.table_name}();")

        self._main_connection.commit()  # push changes to DB

    def _create_columns(self):
        """check Columns and create it if not exists"""

        """
        BUG: there is a bug in PostgreSQL with PRIMARY KEY constraint
        https://www.postgresql.org/message-id/13277.1566920001%40sss.pgh.pa.us
        Thus, this function must be called only once at the start of database usage to avoid this conflict
        Or else it needs more complicated error handling
        """

        # add columns to tables
        for table in self._tables_list:
            try:
                query = ""
                for col_name, col_def in table.table_columns.items():
                    query += f"ALTER TABLE {table.table_name} ADD COLUMN IF NOT EXISTS {col_name} {col_def};\n"

                if table.table_composite_primary_key is not None:
                    key_values = sql.SQL(",").join(sql.Identifier(i) for i in table.table_composite_primary_key)
                    query += f"ALTER TABLE {table.table_name} ADD PRIMARY KEY({key_values.as_string(self._main_cursor)});"

                self._main_cursor.execute(query)
            except Exception as e:
                print(e)

        self._main_connection.commit()  # push changes to DB

    def _recreate_all_tables(self):
        """delete all existing tables and create new tables"""

        for table in DatabaseHandler._tables_list:
            self._main_cursor.execute(f"DROP TABLE IF EXISTS {table.table_name} CASCADE;")

        self._correct_tables()
        self._create_columns()
        self._main_connection.commit()  # push changes to DB

    # database request functions
    def update(self, obj):
        """
        Accepts all objects except User object

        Updates entity for parent_object if it was already created
        Inserts entity for parent_object if it is new in table (if id was not assigned to it at creation point)

        if entity is None, than parent_object is the entity to update or insert

        :param obj: object to update in database
        :return: True if update successful False otherwise
        """
        if self._connected_db:
            if obj.id != -1:
                # obj.id remains the same
                self._query_update_one(obj, {"user_id": obj.user_id})
            else:
                # execute insert query and update object id
                obj.id = self._query_insert_one(obj)

            self._main_connection.commit()
            return obj
        return None

    def delete(self, obj=None):
        """
        Deletes object from database
        :param obj:
        """
        if isinstance(obj, User):
            self._query_delete_one(obj, {"id": obj.id})
        else:
            self._query_delete_one(obj, {"id": obj.id, "user_id": obj.user_id})

        self._main_connection.commit()

    def get_events_for_period(self, user, start: datetime, end: datetime):
        """get all events_list in given date range as list"""
        self._main_cursor.execute(
            sql.SQL(f"SELECT * FROM {Event.table_name} WHERE \"user_id\"=%s AND \"time_start\" BETWEEN %s AND %s;"),
            (user.id, start, end)
        )
        # create Event objects and assing their id's
        events = []
        for values in self._main_cursor.fetchall():
            events.append(Event(*values[1:]))
            events[-1].id = values[0]
        return events

    def get_event_groups(self, user):
        """
        :param user: User object
        :return: list of EventGroup objects with their events_list
        """

        return self._query_left_join_tables(EventGroup,
                                            Event,
                                            ("id", "group_id"),
                                            {f"{EventGroup.table_name}.user_id": user.id},
                                            "events")

    def get_all_event_patterns(self, user):
        """Return all event patterns"""

        return self._query_left_join_tables(EventPattern,
                                            EventParametric,
                                            ("id", "patern_id"),
                                            {f"{EventPattern.table_name}.user_id": user.id},
                                            "events")

    def update_user(self, user: User):
        """
        Updates user if it was already created
        Inserts user if it is new in table (if id was not assigned to it at creation point)

        :param user: user object to update
        :return: reference to 'user' object with updated id
                or None, if connection with database was not established yet
        """

        if self._connected_db:
            if user.id != -1:
                # object id remains the same
                self._query_update_one(user, {"id": user.id})
            else:
                # execute insert query and update user id
                user.id = self._query_insert_one(user)

            self._main_connection.commit()
            return user
        return None

    def delete_user(self, user: User):
        """
        Deletes entry from User table and cascade delete all connected entries
        :param user: User object to delete
        """
        self._query_delete_one(user, {"id": user.id})

    def _query_left_join_tables(self,
                                table_left: DatabaseSavable, table_right: DatabaseSavable,
                                fields_pair, filter_dict, table_left_list_attr_name):
        """
        Performs join query with two tables
        Collects all values from second table to list field from left table

        :param table_left: table that contains list of objects from right table
        :param table_right: child objects table for first table
        :param fields_pair: tuple of two fields to match in JOIN ON query
        :param filter_dict: filter dictionary to find all tables with correct fields
        :param table_left_list_attr_name: attribute name of list in object from left table
        :return: object list from left table with lists of objects from right table
        """

        query = f"SELECT * FROM {table_left.table_name} LEFT JOIN {table_right.table_name} "\
                f"ON {table_left.table_name}.{fields_pair[0]} = {table_right.table_name}.{fields_pair[1]} " \
                f"WHERE {self._and_clause_from_dict_raw_name(filter_dict)};"
        self._main_cursor.execute(query)

        return self.split_left_join_results(table_left, table_left_list_attr_name, table_right)

    def split_left_join_results(self, table_left, table_right, table_left_list_attr_name):
        """
        Splits rows from previous left join query using left and right table data

        :param table_left: left table class object
        :param table_right: right table class object
        :param table_left_list_attr_name: attribute name for list inside left table object
        :return:
        """

        object_left_line_end = len(table_left.table_columns)
        object_right_line_end = object_left_line_end + len(table_right.table_columns)

        objects = []
        for cursor_line in self._main_cursor.fetchall():
            cur_object_left = table_left.from_table_values(
                cursor_line[0: object_left_line_end]
            )

            cur_object_right = table_right.from_table_values(
                cursor_line[object_left_line_end: object_right_line_end]
            )

            last_object = objects[-1] if len(objects) > 0 else None
            if cur_object_left == last_object:
                object_left_list = getattr(last_object, table_left_list_attr_name)
                object_left_list.append(cur_object_right)
            else:
                object_left_list = getattr(cur_object_left, table_left_list_attr_name)
                object_left_list.append(cur_object_right)
                objects.append(cur_object_left)

        return objects

    def _query_insert_one(self, obj):
        """
        Executes INSERT query with object fields and values

        :param obj: object to insert
        :return: id of newly created object
        """
        values = obj.get_values()

        keys_str = sql.SQL(', ').join(
            map(sql.Identifier,
                (key for key, val in values if key != "id"))
        ).as_string(self._main_cursor)

        values_str = sql.SQL(', ').join(
            map(sql.Literal,
                (val for key, val in values if key != "id"))
        ).as_string(self._main_cursor)

        self._main_cursor.execute(
            f"INSERT INTO {obj.table_name}({keys_str})\n"
            f"VALUES ({values_str}) "
            "RETURNING id;"
        )
        return self._main_cursor.fetchone()[0]

    def _and_clause_from_dict(self, field_dict: dict):
        return sql.SQL(" AND ").join(
            sql.Identifier(name) + sql.SQL(" = ") + sql.Literal(value)
            for name, value in field_dict.items()
        ).as_string(self._main_cursor)

    def _and_clause_from_dict_raw_name(self, field_dict: dict):
        return sql.SQL(" AND ").join(
            sql.SQL(name) + sql.SQL(" = ") + sql.Literal(value)
            for name, value in field_dict.items()
        ).as_string(self._main_cursor)

    def _query_update_one(self, obj, search_dict: dict, values_dict: dict = None):
        """
        This function contains UPDATE query which searches for specific value of a field
        and updates contents of matching object using _main_cursor

        :param obj: object which will be updated
        :param search_dict: dictionary of field:value pairs to search inside query
        :param values_dict: values to update inside current object,
                if values is None, all columns for current object will be updated
        """

        if values_dict is None:
            values_dict = obj.get_values()

        set_fields_string = sql.SQL(', ').join(
            map(lambda elem: (
                sql.SQL("{0}={1}").format(
                    sql.Identifier(elem[0]),
                    sql.Literal(elem[1]))
            ),
                (elem for elem in values_dict.items() if elem[0] != "id" and elem[0] not in search_dict))
        ).as_string(self._main_cursor)
        query = f"UPDATE {obj.table_name}\nSET {set_fields_string}\nWHERE {self._and_clause_from_dict(search_dict)};"

        self._main_cursor.execute(query)

    def _query_delete_one(self, obj, field_dict: dict):
        """

        :param obj: object to delete
        :param field_dict: dictionary of field:value pairs to search for query
        """

        query = f"DELETE FROM {obj.table_name} WHERE {self._and_clause_from_dict(field_dict)};"
        self._main_cursor.execute(query)

    def update_fields(self, obj, fields: list):
        """
        Updates only specifyed fields for given object
        :param obj: object to update
        :param fields: list of strings with field names
        """
        values = {}
        for field in fields:
            if field not in obj.__dict__:
                raise ValueError(f"Wrong attribute name specifyed {field}")

            values[field] = getattr(obj, field)

        if len(values) > 0:
            self._query_update_one(obj, {"id": obj.id}, values)
