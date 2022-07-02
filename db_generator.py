from testy.models import *
import random
import string
import datetime
from random import randint, randrange, uniform
import urllib, json
import urllib.request

query_ALL_ROWS= ('SELECT SUM(Rows_n) FROM '
                '(WITH tbl AS '
                '(SELECT table_schema, '
                'TABLE_NAME '
                'FROM information_schema.tables '
                'WHERE TABLE_NAME not like \'pg_%%\' '
                'AND table_schema in (\'public\')) '
                'SELECT table_schema, '
                'TABLE_NAME, '
                '(xpath(\'/row/c/text()\', query_to_xml(format(\'select count(*) as c from %%I.%%I\', table_schema, TABLE_NAME), FALSE, TRUE, \'\')))[1]::text::int AS rows_n '
                'FROM tbl '
                'ORDER BY rows_n DESC)liczba ')

class DBGenerator():
    def __init__(self):
        print('\nConnecting to \'' + db.engine.name + '\'...',end='\r')
        self.db = DBConnection()
        print('\r\t\t\t\tdone')
        self.users = []
        self.sp_array=[]
        self.hr_array=[]

    def cleanDB(self):
        print('Drop all...', end='\r')
        self.db._engine.drop_all()
        print('\r\t\t\t\tdone')
        print('Create all...',end='\r')
        self.db._engine.create_all()
        print('\r\t\t\t\tdone')

    def createDB(self):
        print('Create countries...',end='\r')
        self.createCountries()
        print('')
        print('Create roles...',end='\r')
        self.createRoles()
        print('\r\t\t\t\tdone')
        print('Create genders...',end='\r')
        self.createGenders()
        print('\r\t\t\t\tdone')
        print('Create avatars...',end='\r')
        self.createAvatars()
        print('\r\t\t\t\tdone')
        print('Create users...',end='\r')
        self.createUsers(results=20)
        print('')
        print('Create measurements...',end='\r')
        self.createMeasurements()
        print('')

    def doQuery(self):
        try:
            resultproxy = db.engine.execute(query_ALL_ROWS)
            result = [dict(row) for row in resultproxy]
            print('All rows in database: '+ str(result[0]['sum']))
        except:
            print('Finished')

        
    def randomHash(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def createCountries(self):
        url = "https://restcountries.com/v3.1/all"
        json_url = urllib.request.urlopen(url)
        data = json.loads(json_url.read())
        commonList=[]
        for x in data:
            commonList.append(x['name']['common'])
        commonList = sorted(commonList)
        i=1
        for x in commonList:
            self.db.session.add(Country(name=x))
            if (i-1)%30==0:
                self.db.Flush()
            print('\r\t\t\t\t['+str(i)+'/'+str(len(commonList))+']', end='\r') 
            i+=1
        
    def createRoles(self):
        self.db.session.add(UserRole(name=UserRole.BASIC))
        self.db.session.add(UserRole(name=UserRole.ADMIN))
        self.db.Flush()

    def createGenders(self):
        self.db.session.add(Gender(name=Gender.MALE))
        self.db.session.add(Gender(name=Gender.FEMALE))
        self.db.Flush()

    def createAvatars(self):
        self.db.session.add(Avatar(name=Avatar.DEFAULT))
        self.db.session.add(Avatar(
            name='media/pvwhl1clmfmymuy7pwls',
            options="{\"height\": \"1007\", \"width\": \"1007\", \"x\": \"88\", \"y\": \"80\"}"))
        self.db.session.add(Avatar(
            name='media/hiyyt5yyd8fcwrnp5zft',
            options="{\"height\": \"702\", \"width\": \"702\", \"x\": \"273\", \"y\": \"0\"}"))
        self.db.Flush()

    def createUsers(self, results):
        i = 1
        url = "https://randomuser.me/api/?results="+ str(results) +"&inc=gender,name,location,email,login,dob&password=upper,lower,special,number,8-16&noinfo"
        json_url = urllib.request.urlopen(url)
        users = json.loads(json_url.read())
        for user in users['results']:
            profile = UserProfile(first_name = user['name']['first'], last_name = user['name']['last'], 
                                gender_id = Gender.query.filter_by(name=user['gender']).first().id,
                                dob = datetime.datetime.strptime(user['dob']['date'],"%Y-%m-%dT%H:%M:%S.%fZ"), 
                                nationality_id = Country.query.filter_by(name=user['location']['country']).first().id,
                                height = randrange(120,200), weight = randrange(40,150))
            dashboard = Dashboard()
            user = User(username = user['login']['username'], email = user['email'], password = user['login']['password'])
            user.dashboards = dashboard
            user.profiles = profile
            self.db.session.add(user)
            self.db.Flush()
            print('\r\t\t\t\t['+str(i)+'/'+str(len(users['results']))+']', end='\r') 
            i+=1

        profile1 = UserProfile(first_name = "Adrian", last_name = "Bejs", gender_id = 1, 
                                nationality_id = Country.query.filter_by(name='Poland').first().id,
                                dob = datetime.datetime.strptime('24051986', "%d%m%Y").date(),
                                avatar_id = 3, height = 181, weight = 95)
                                
        profile2 = UserProfile(first_name = "Mateusz", last_name = "Kowalski", gender_id = 1,
                                nationality_id = Country.query.filter_by(name='Poland').first().id,
                                dob = datetime.datetime.strptime('12101986', "%d%m%Y").date(), 
                                avatar_id = 2, height = 183, weight = 65)   

        dashboard1 = Dashboard()
        dashboard2 = Dashboard()

        admin1 = User(username="Hantal", email = "adrianbejs@gmail.com",  password = "12345678", roleId = 2)
        admin2 = User(username="NoaniX", email = "mateuszpe@gmail.com", password = "12345678", roleId = 2)

        admin1.dashboards = dashboard1
        admin2.dashboards = dashboard2
        admin1.profiles = profile1
        admin2.profiles = profile2
        self.db.AddUser(admin1)
        self.db.AddUser(admin2)
        self.db.session.add(admin1)
        self.db.session.add(admin2)
        self.db.Flush()

    def createMeasurements(self):
        i=1
        user = User.query.filter_by(username='NoaniX').first()
        for x in range(31*3):
            current_time = datetime.datetime.utcnow()
            day = current_time - datetime.timedelta(days=31-(x/3), hours=randint(7,14), minutes=randint(0,60))
            new_measurement = Measurement(day)
            for x in range(19):
                sp=round(uniform(90,99),4)
                hr=round(uniform(60,120),6)
                #disabled for better performance
                #new_measurement.sp_data.append(Sp_data(data=sp)) 
                #new_measurement.hr_data.append(Hr_data(data=hr)) 
                self.sp_array.append(sp)
                self.hr_array.append(hr)
            new_measurement.hr_data_avg = sum(self.sp_array) / len(self.sp_array)
            new_measurement.sp_data_avg = sum(self.hr_array) / len(self.hr_array)
            user.profiles.measurements.append(new_measurement)
            self.sp_array = []
            self.hr_array = []
            if (i-1)%10==0:
                self.db.Flush()
            print('\r\t\t\t\t['+str(i)+'/93]', end='\r')  
            i+=1

    def randomDate(self):
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
    generator.doQuery()
