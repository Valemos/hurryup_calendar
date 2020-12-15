from application.user import User
from database.database_savable import DatabaseSavable

class EventGroup(DatabaseSavable):

    table_name = "\"EventGroup\""

    table_columns = {
        "id":           "SERIAL PRIMARY KEY",
        "user_id":      f"INTEGER REFERENCES {User.table_name}(id) ON DELETE CASCADE",
        "name":         "VARCHAR(64) NOT NULL",
        "description":  "TEXT",
        "done":         "BOOLEAN"
    }

    def __init__(self, user_id, name, description='', done=False, events=None):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.done = done
        self.events = events if events is not None else []
