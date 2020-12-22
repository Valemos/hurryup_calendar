from application.account_type import AccountType
from database.database_savable import DatabaseSavable


class User(DatabaseSavable):

    table_name = '"user"'

    table_columns = {
        'id':               "SERIAL PRIMARY KEY",
        'name':             "VARCHAR(64) NOT NULL",
        'login':            "VARCHAR(128) UNIQUE NOT NULL",
        'email':            "VARCHAR(128) NOT NULL",
        'password_hash':    "VARCHAR(256) NOT NULL",
        'account_type':     "INTEGER DEFAULT 0",
        'image_url':        "TEXT"
    }

    def __init__(self,
                 name='',
                 login='',
                 email='',
                 password_hash='',
                 account_type=AccountType.User,
                 image_url=''):
        super().__init__()
        self.name = name
        self.login = login
        self.email = email
        self.password_hash = password_hash
        self.account_type = account_type.value
        self.image_url = image_url

    def __eq__(self, other):
        if super().__eq__(other):
            return self.login == other.login

    def update_db(self, database):
        database.update_user(self)

    def delete_db(self, database):
        database.delete_user(self)


