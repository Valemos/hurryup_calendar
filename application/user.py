import enum

class AccountType(enum.Enum):
    User = 0,
    Admin = 1


class User:

    def __init__(self, name, login, email, password_hash, account_type=AccountType.User, image_url=''):
        self.name = name
        self.login = login
        self.email = email
        self.password_hash = password_hash
        self.account_type = account_type.value
        self.image_url = image_url
