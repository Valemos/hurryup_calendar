from datetime import datetime, timedelta


class Event:

    def __init__(self,
                 user,
                 time_start: datetime,
                 time_end: datetime,
                 name='', description='',
                 event_group_id=None,
                 done=False):
        self.user = user
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.description = description
        self.event_group_id = event_group_id
        self.done = done

    def move_by_period(self, delta: timedelta):
        self.time_start += delta
        self.time_end += delta
