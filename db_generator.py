from testy.models import *
import random
import string


class DBGenerator():
    def __init__(self):
        self.db = DBConnection()
        self.users = []

    def cleanDB(self):
        self.db._engine.drop_all()
        self.db._engine.create_all()

    def createDB(self):
        self.createUsers()

    def randomHash(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def createUsers(self):
        usernames = ["Adrian","Adam","Tomasz","Wiktoria","Aleksander",
                    "Nastia","Mateusz","Piotr","Bartek", "Ola", "Karolina", "Kasia",
                    "Natalia", "Krzysztof", "Jan"]
        admin1 = User(username="Hantal", email = "adrianbejs@gmail.com", 
                password_hash=self.randomHash(60),
                role_id = 2)
        admin2 = User(username="NoaniX", email = "mateuszpe@gmail.com", 
                password_hash=self.randomHash(60),
                role_id = 2)
        self.db.AddUser(admin1)
        self.users.append(admin1)
        self.db.AddUser(admin2)
        self.users.append(admin2)
        for user in usernames:
            user = User(username = user, email = user + "@gmail.com", 
                    password_hash = self.randomHash(60), role_id = 1)
            self.db.AddUser(user)
            self.users.append(user)
        self.db.Flush()

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.createDB()
