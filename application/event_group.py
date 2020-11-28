class EventGroup:

    def __init__(self, user, name, description='', events=None):
        if events is None:
            events = []

        self.user = user
        self.user_id = user.id
        self.name = name
        self.description = description
        self.done = False
        self.events = events
