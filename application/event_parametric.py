from datetime import datetime

class EventParametric:

    def __init__(self, user: User, start_time: datetime, end_time: datetime, name, description=''):
        super().__init__()
        self.user = user
        self.start_time = start_time
        self.end_time = end_time

        self.name = name
        self.description = description
