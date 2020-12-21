import enum
from abc import ABC
from datetime import datetime
import psycopg2
import psycopg2.sql as sql

from application.event import Event
from application.event_group import EventGroup
from application.event_parametric import EventParametric
from application.event_pattern import EventPattern
from application.user import User
from database.database_savable import DatabaseSavable


class DatabaseHandler:
    _tables_list = [User, EventGroup, Event, EventPattern, EventParametric]

    def __init__(self,
                 new_name="CalendarApp",
                 new_pass="1",
                 new_port="5432",
                 new_host="localhost",
                 new_user="postgres"):

        self._name_db = new_name
        self._pass_db = new_pass
        self._port_db = new_port
        self._host_db = new_host
        self._user_db = new_user
        self._main_connection = None

        self._connected_state = self._try_connect_db()

    def __del__(self):
        if self._main_connection is not None:
            self._main_connection.close()

    def _try_connect_db(self):
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
        return self._connected_state

    def _correct_tables(self):
        """check Tables and create it if not exists"""

        # check every table and create if not exists
        for table in DatabaseHandler._tables_list:
            self._main_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table.table_name}();")

        self._main_connection.commit()

    def _create_columns(self):
        """
        there is a bug in PostgreSQL with altering PRIMARY KEY constraint !
        https://www.postgresql.org/message-id/13277.1566920001%40sss.pgh.pa.us
        Thus, this function must be called only once at the start of database usage to avoid this conflict
        Or else it needs more complicated error handling
        """

        for table in self._tables_list:
            try:
                query = ""
                for col_name, col_def in table.table_columns.items():
                    query += f"ALTER TABLE {table.table_name} ADD COLUMN IF NOT EXISTS {col_name} {col_def};\n"

                self._main_cursor.execute(query)
            except Exception as e:
                print(e)

        self._main_connection.commit()

    def _recreate_all_tables(self):
        for table in DatabaseHandler._tables_list:
            self._main_cursor.execute(f"DROP TABLE IF EXISTS {table.table_name} CASCADE;")

        self._correct_tables()
        self._create_columns()
        self._main_connection.commit()

    # database request functions
    def update(self, obj):
        """
        Accepts all objects except User object
        Only User object don't have "user_id" column
        """
        if self._connected_state:
            if obj.id != -1:
                # obj.id remains the same
                self._query_update_one(obj, {"id": obj.id})
            else:
                # execute insert query and update object id
                obj.id = self._query_insert_one(obj)

            return obj
        return None

    def delete(self, obj=None):
        """
        Accepts all objects except User object
        Only User object don't have "user_id" column
        """
        if isinstance(obj, User):
            self._query_delete_one(obj, {"id": obj.id})
        else:
            self._query_delete_one(obj, {"id": obj.id, "user_id": obj.user_id})

        self._main_connection.commit()

    def get_events_for_period(self, user, start: datetime, end: datetime):
        self._main_cursor.execute(
            sql.SQL(f'SELECT * FROM {Event.table_name} WHERE "user_id"=%s AND "time_start" BETWEEN %s AND %s;'),
            (user.id, start, end)
        )
        s = sql.SQL(f"SELECT * FROM {Event.table_name} WHERE \"user_id\"={{0}} AND \"time_start\" BETWEEN {{1}} AND {{2}};").format(
            sql.Literal(user.id), sql.Literal(start), sql.Literal(end)).as_string(self._main_cursor)
        events = []
        for values in self._main_cursor.fetchall():
            events.append(Event.from_table_values(values))

        return events

    def get_event_groups(self, user):
        return self._query_left_join_tables(
            EventGroup, Event,
            match_fields=("id", "group_id"),
            filter_dict={f"{EventGroup.table_name}.user_id": user.id},
            list_attribute_name="events")

    def get_event_patterns(self, user):
        return self._query_left_join_tables(
            EventPattern, EventParametric,
            match_fields=("id", "patern_id"),
            filter_dict={f"{EventPattern.table_name}.user_id": user.id},
            list_attribute_name="events")

    def update_user(self, user: User):
        if self._connected_state:
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
        self._query_delete_one(user, {"id": user.id})

    def _query_left_join_tables(self,
                                table_left: DatabaseSavable, table_right: DatabaseSavable,
                                match_fields, filter_dict, list_attribute_name):
        """
        match_fields: tuple of two fields to match in JOIN ON query
        filter_dict: filter dictionary to find all tables with correct fields
        """

        query = f"SELECT * FROM {table_left.table_name} LEFT JOIN {table_right.table_name} "\
                f"ON {table_left.table_name}.{match_fields[0]} = {table_right.table_name}.{match_fields[1]} " \
                f"WHERE {self._and_clause_from_dict_raw_name(filter_dict)};"
        self._main_cursor.execute(query)
        self._main_connection.commit()

        return self._split_left_join_results(table_left, table_right, list_attribute_name)

    def _split_left_join_results(self, table_left, table_right, list_attribute_name):
        object_left_line_end = len(table_left.table_columns)
        object_right_line_end = object_left_line_end + len(table_right.table_columns)

        object_tables = (table_left, table_right)
        object_line_ends = (object_left_line_end, object_right_line_end)

        objects = []
        for cursor_line in self._main_cursor.fetchall():
            line_objects = self._split_cursor_line(cursor_line, object_tables, object_line_ends)

            cur_object_left = line_objects[0]
            cur_object_right = line_objects[1]

            # appends right object to left object's list or appends new left object
            last_object = objects[-1] if len(objects) > 0 else None
            if cur_object_left == last_object:
                object_left_list = getattr(last_object, list_attribute_name)
                object_left_list.append(cur_object_right)
            else:
                object_left_list = getattr(cur_object_left, list_attribute_name)
                object_left_list.append(cur_object_right)
                objects.append(cur_object_left)

        return objects

    @staticmethod
    def _split_cursor_line(cursor_line, tables, object_ends):
        objects = []
        beginning = 0
        for table, end in zip(tables, object_ends):
            new_object = table.from_table_values(cursor_line[beginning: end])
            objects.append(new_object)
            beginning = end
        return objects

    def _query_insert_one(self, obj):
        values = obj.get_values()

        keys_str = sql.SQL(', ').join(
            map(sql.Identifier,
                (key for key, val in values.items() if key != "id"))
        ).as_string(self._main_cursor)

        values_str = sql.SQL(', ').join(
            map(sql.Literal,
                (val for key, val in values.items() if key != "id"))
        ).as_string(self._main_cursor)

        self._main_cursor.execute(
            f"INSERT INTO {obj.table_name}({keys_str})\n"
            f"VALUES ({values_str}) "
            "RETURNING id;"
        )
        self._main_connection.commit()
        return self._main_cursor.fetchone()[0]

    def _and_clause_from_dict(self, field_dict: dict):
        # preferred function to use for general cases
        return sql.SQL(" AND ").join(
            sql.Identifier(name) + sql.SQL(" = ") + sql.Literal(value)
            for name, value in field_dict.items()
        ).as_string(self._main_cursor)

    def _and_clause_from_dict_raw_name(self, field_dict: dict):
        # this function will not add brackets to name and use it as is
        return sql.SQL(" AND ").join(
            sql.SQL(name) + sql.SQL(" = ") + sql.Literal(value)
            for name, value in field_dict.items()
        ).as_string(self._main_cursor)

    def _query_update_one(self, obj, search_dict: dict, values_dict: dict = None):
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
        self._main_connection.commit()

    def _query_delete_one(self, obj, field_dict: dict):
        query = f"DELETE FROM {obj.table_name} WHERE {self._and_clause_from_dict(field_dict)};"
        self._main_cursor.execute(query)
        self._main_connection.commit()

    def update_fields(self, obj, fields: list):
        values = {}
        for field in fields:
            if field not in obj.__dict__:
                raise ValueError(f"Wrong attribute name specifyed {field}")

            values[field] = getattr(obj, field)

        if len(values) > 0:
            self._query_update_one(obj, {"id": obj.id}, values)
