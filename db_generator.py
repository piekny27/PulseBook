from testy.models import *
import random
import string
import datetime
from random import randint, randrange, uniform

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

    def createUsers(self):
        i = 1
        usernames = ["Adrian","Adam","Tomasz","Wiktoria","Aleksander",
                    "Nastia","Mateusz","Piotr","Bartek", "Ola", "Karolina", "Kasia",
                    "Natalia", "Krzysztof", "Jan"]
        for user in usernames:
            profile = UserProfile(first_name = user, last_name = "Kowalski",
                                date_of_birth = self.randomDate(), gender = "Male", 
                                nationality = "Polska", avatarName = "avatar" + i,
                                height = randrange(120,200), weight = randrange(40,150))
            self.db.AddProfile(profile)
            self.db.Flush()

            dashboard = Dashboard()
            self.db.AddDashboard(dashboard)
            self.db.Flush()

            user = User(username = user, email = user + "@gmail.com", passwordHash = self.randomHash(60), 
                    roleId = 1, profileId = profile.id, deviceId = i, dashboard_id = dashboard.id)
            self.db.AddUser(user)
            i+=1
            self.users.append(user)

        profile1 = UserProfile(first_name = "Adrian", last_name = "Bejs", gender = "Male", nationality = "Polska",
                                date_of_birth = datetime.datetime.strptime('24051986', "%d%m%Y").date(),
                                avatarName = "avatar01", height = 181, weight = 95)
                                
        profile2 = UserProfile(first_name = "Mateusz", last_name = "Kowalski", gender = "Male", nationality = "Polska",
                                date_of_birth = datetime.datetime.strptime('12101986', "%d%m%Y").date(), 
                                avatarName = "avatar01", height = 183, weight = 65)   

        self.db.AddProfile(profile1)
        self.db.AddProfile(profile2)
        self.db.Flush()

        dashboard1 = Dashboard()
        self.db.AddDashboard(dashboard)
        self.db.Flush()
        dashboard2 = Dashboard()
        self.db.AddDashboard(dashboard)
        self.db.Flush()

        admin1 = User(username="Hantal", email = "adrianbejs@gmail.com",  password = "12345678", 
            roleId = 2, profileId = profile1.id, deviceId = i, dashboard_id = dashboard1.id)

        i+=1

        admin2 = User(username="NoaniX", email = "mateuszpe@gmail.com", 
                password = "12345678",
                roleId = 2, profileId = profile2.id, deviceId = i, dashboard_id = dashboard2.id)
        
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
                #self.db.Flush() 
            new_measurement.hr_data_avg = sum(self.sp_array) / len(self.sp_array)
            new_measurement.sp_data_avg = sum(self.hr_array) / len(self.hr_array)
            user = User.query.filter_by(id=17).first()
            user.profiles.measurements.append(new_measurement)
            self.sp_array = []
            self.hr_array = []
            db.session.commit()  

    def randomDate():
        start_date = datetime.date(1960, 1, 1)
        end_date = datetime.date(2001, 1, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_number_of_days)

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.createDB()
