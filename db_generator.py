from xmlrpc.client import DateTime
from testy.models import *
import random
import string
import datetime


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
        profile1 = UserProfile(first_name = "Mateusz", last_name = "Kowalski",
                                date_of_birth = datetime.datetime.now(), age = 23,
                                gender = "Male", nationality = "Polska", avatarName = "avatar01",
                                height = 183, weight = 65)
        profile2 = UserProfile(first_name = "Adrian", last_name = "Bejs",
                                date_of_birth = datetime.datetime.now(), age = 22,
                                gender = "Male", nationality = "Polska", avatarName = "avatar01",
                                height = 181, weight = 68)
        usernames = ["Adrian","Adam","Tomasz","Wiktoria","Aleksander",
                    "Nastia","Mateusz","Piotr","Bartek", "Ola", "Karolina", "Kasia",
                    "Natalia", "Krzysztof", "Jan"]
        admin1 = User(username="Hantal", email = "adrianbejs@gmail.com", 
                password = "12345678",
                roleId = 2, profileId = 1)
        admin2 = User(username="NoaniX", email = "mateuszpe@gmail.com", 
                password = "12345678",
                roleId = 2, profileId = 2)
        self.db.AddProfile(profile1)
        self.db.AddUser(admin1)
        self.users.append(admin1)
        self.db.AddProfile(profile2)
        self.db.AddUser(admin2)
        self.users.append(admin2)
        for user in usernames:
            user = User(username = user, email = user + "@gmail.com", 
                    passwordHash = self.randomHash(60), roleId = 1, profileId = 2)
            self.db.AddUser(user)
            self.users.append(user)
        self.db.Flush()

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.createDB()
