class BucketList():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.activities = []
        self.no_of_activities = len(self.activities)

    def add_activity(self, activity):
        self.activities.append(activity)
        return True

    def delete_activity(self, activity):
        pass

class Activity():
    pass

class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password