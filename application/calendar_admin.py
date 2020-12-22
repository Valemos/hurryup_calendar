from application.account_type import AccountType
from application.user import User
from database.database_handler import DatabaseHandler


class CalendarAdmin:

    class NotAdminUserException(Exception):
        pass

    def __init__(self, user_admin: User, database_handler=None):

        if AccountType(user_admin.account_type) is not AccountType.Admin:
            raise CalendarAdmin.NotAdminUserException

        self.user_admin = user_admin
        self.database_handler: DatabaseHandler = database_handler if database_handler is not None else DatabaseHandler()

        # check connection to database here
        if not self.database_handler.check_connected():
            print("Application not connected to database")

