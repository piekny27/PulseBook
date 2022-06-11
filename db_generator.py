from xmlrpc.client import DateTime
from testy.models import *
import random
import string
import datetime
from random import randint, uniform

class DBGenerator():
    def __init__(self):
        self.db = DBConnection()
        self.users = []
        self.sp_array=[]
        self.hr_array=[]

    def cleanDB(self):
        self.db._engine.drop_all()
        self.db._engine.create_all()

    def createDB(self):
        self.createDevices()
        self.createRoles()
        self.createProfiles()
        self.createUsers()
        self.createMeasurements()
        

    def randomHash(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def createDevices(self):
        for x in range(17):
            self.db.session.add(Device(serial_number = self.randomHash(5)))

    def createRoles(self):
        self.db.session.add(UserRole(name=UserRole.BASIC))
        self.db.session.add(UserRole(name=UserRole.ADMIN))

    def createProfiles(self):
        profile1 = UserProfile(first_name = "Ludzie", last_name = "Wszyscy",
                                date_of_birth = datetime.datetime.now(), age = 22,
                                gender = "Male", nationality = "Polska", avatarName = "avatar01",
                                height = 181, weight = 68)
        profile2 = UserProfile(first_name = "Adrian", last_name = "Bejs",
                                date_of_birth = datetime.datetime.now(), age = 22,
                                gender = "Male", nationality = "Polska", avatarName = "avatar01",
                                height = 181, weight = 68)
        profile3 = UserProfile(first_name = "Mateusz", last_name = "Bjuti",
                                date_of_birth = datetime.datetime.now(), age = 23,
                                gender = "Male", nationality = "Polska", avatarName = "avatar01",
                                height = 183, weight = 65)   
        self.db.AddProfile(profile1)
        self.db.AddProfile(profile2)
        self.db.AddProfile(profile3)

    def createUsers(self):
        i = 1
        usernames = ["Adrian","Adam","Tomasz","Wiktoria","Aleksander",
                    "Nastia","Mateusz","Piotr","Bartek", "Ola", "Karolina", "Kasia",
                    "Natalia", "Krzysztof", "Jan"]
        for user in usernames:
            user = User(username = user, email = user + "@gmail.com", 
                    passwordHash = self.randomHash(60), roleId = 1, profileId = 1, deviceId = i)
            self.db.AddUser(user)
            i+=1
            self.users.append(user)

        admin1 = User(username="Hantal", email = "adrianbejs@gmail.com", 
                password = "12345678",
                roleId = 2, profileId = 2, deviceId = i)
        i+=1
        admin2 = User(username="NoaniX", email = "mateuszpe@gmail.com", 
                password = "12345678",
                roleId = 2, profileId = 3, deviceId = i)
        self.db.AddUser(admin1)
        self.users.append(admin1)
        self.db.AddUser(admin2)
        self.users.append(admin2)
        self.db.Flush()

    def createMeasurements(self):
        for x in range(31*3):
            current_time = datetime.datetime.utcnow()
            day = current_time - datetime.timedelta(days=31-(x/3), hours=randint(7,14), minutes=randint(0,60))
            new_measurement = Measurement(day)
            for x in range(19):
                sp=round(uniform(90,99),4)
                hr=round(uniform(60,120),6)
                new_measurement.sp_data.append(Sp_data(data=sp)) 
                new_measurement.hr_data.append(Hr_data(data=hr)) 
                self.sp_array.append(sp)
                self.hr_array.append(hr)
                self.db.Flush() 
            new_measurement.hr_data_avg = sum(self.sp_array) / len(self.sp_array)
            new_measurement.sp_data_avg = sum(self.hr_array) / len(self.hr_array)
            user = User.query.filter_by(id=17).first()
            user.profiles.measurements.append(new_measurement)
            self.sp_array = []
            self.hr_array = []
            db.session.commit()  

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.createDB()
