class UserData:
    def __init__(self, id) -> None:
        self.id = id

    def login(self, db_user):
        self.data = db_user
        self.id = db_user.id
