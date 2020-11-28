from application.user import DatabaseSavable

class EventPattern:

    def __init__(self, user, name, description='', events=None):

        if events is None:
            self.events = []
        else:
            self.events = events

        self.user = user
        self.name = name
        self.description = description

    def add_event(self, event, database):
        self.events.append(event)
        database.update(self.user, event)
