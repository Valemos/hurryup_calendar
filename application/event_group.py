from application.user import User
from database.database_savable import DatabaseSavable

class EventGroup(DatabaseSavable):

    table_name = "eventgroup"

    table_columns = {
        "id":           "SERIAL PRIMARY KEY",
        "name":         "VARCHAR(64) NOT NULL",
        "description":  "TEXT",
        "done":         "BOOLEAN",
        "user_id":      f"INTEGER REFERENCES {User.table_name}(id) ON DELETE CASCADE"
    }

    def __init__(self,
                 name='',
                 description='',
                 done=False,
                 user_id=-1,
                 events=None):

        super().__init__()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.done = done
        self.events = events if events is not None else []
