from application.account_type import AccountType
from application.user import User

class CalendarAdmin:

    class NotAdminUserException(Exception):
        pass

    def __init__(self, user_admin: User):

        if AccountType(user_admin.account_type) is not AccountType.Admin:
            raise CalendarAdmin.NotAdminUserException

        self.user_admin = user_admin
