import datetime
from flask_login import current_user
import jsonpickle
import json
import math


class Dashboard:
    def __init__(self, user=None, range=None):
        self.cards = []
        if user is None:
            self.createCards()
        else:
            self.load(user)
            for card in self.cards:
                card.update(range)

    def toJSON(self):
        return jsonpickle.encode(self)

    def createCards(self):
        self.cards.append(Chart_card())
        self.cards.append(Bmi_card())

    def load(self, user):
        dashboardJSON = DashboardModel.query.filter_by(id=user.dashboard_id).first().json_data
        obj = jsonpickle.decode(dashboardJSON)
        if hasattr(obj, 'cards'):
            self.cards = obj.cards
        else:
            self.createCards()

class Chart_card:
    def __init__(self):
        self.card_type = 'chart_measurement_card.html'
        self.range = "last_week"
        self.measurements = self.get_measurementsJSON()
        if self.measurements is None or self.measurements == '[]':
            self.msg = 'You don\'t have any measurements. Configure your device in settings page and take your first measurement'
        else:
            self.msg = 'The chart shows your measurements for the selected time range.'

    def get_measurementsJSON(self):
        measurements = None
        if not current_user:
            return None
        if not current_user.is_authenticated:
            return None
        match self.range:
                case 'last_5':
                    current_time = datetime.datetime.utcnow()
                    measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.order_by(Measurement.id.desc()).limit(5).all()
                case 'last_week':
                    current_time = datetime.datetime.utcnow()
                    day_ago = current_time - datetime.timedelta(weeks=1)
                    measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
                case 'last_month':
                    current_time = datetime.datetime.utcnow()
                    day_ago = current_time - datetime.timedelta(weeks=4)
                    measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
                case _:
                    current_time = datetime.datetime.utcnow()
                    day_ago = current_time - datetime.timedelta(weeks=1)
                    measurements = UserProfile.query.filter_by(id=current_user.profileId).first().measurements.filter(Measurement.date > day_ago).all()
        new_m = []
        for measurement in measurements:
            new_m.append({'date':measurement.date.isoformat(),'hr_val':measurement.hr_data_avg,'sp_val':measurement.sp_data_avg})
        return json.dumps(new_m)

    def update(self, range=None):
        if range is not None:
            self.range = range
        self.measurements = self.get_measurementsJSON()

class Last_measurement_card:
    def __init__(self, sp_val, hr_val, date):
        self.card_type = 'last_measurement_card.html'
        self.last_measure_sp = sp_val
        self.last_measure_hr = hr_val
        self.date = date

class Bmi_card:
    def __init__(self):
        self.card_type = 'bmi_card.html'
        self.bmi_val = self.calc_bmi()
        self.create_descr()

    def update(self, range=None):
        self.bmi_val = self.calc_bmi()
        self.create_descr()

    def create_descr(self):
        if not self.bmi_val:
            self.bmi_cat = None
            self.bmi_col = 'gray'
            self.bmi_msg = "You need to complete your profile."
        elif self.bmi_val < 16:
            self.bmi_cat = 'Severe Thinness'
            self.bmi_col = 'red'
            self.bmi_msg = 'You have a very low BMI, you should consult your doctor.'
        elif self.bmi_val > 16 and self.bmi_val < 17:
            self.bmi_cat = 'Moderate Thinness'
            self.bmi_col = 'orange'
            self.bmi_msg = 'Pay attention to your diet so that you can make an appointment with a dietitian.'
        elif self.bmi_val > 17 and self.bmi_val < 18.5:
            self.bmi_cat = 'Mild Thinness'
            self.bmi_col = 'yellow'
            self.bmi_msg = 'Almost all right, a little extra weight will keep you healthy.'
        elif self.bmi_val > 18.5 and self.bmi_val < 25:
            self.bmi_cat = 'Normal'
            self.bmi_col = 'green'
            self.bmi_msg = 'You have a perfect bmi, nothing more nothing less.'
        elif self.bmi_val > 25 and self.bmi_val < 30:
            self.bmi_cat = 'Overweight'
            self.bmi_col = 'yellow'
            self.bmi_msg = 'You are slightly overweight, perhaps stop snacking at night.'
        elif self.bmi_val > 30 and self.bmi_val < 35:
            self.bmi_cat = 'Obese Class I'
            self.bmi_col = 'orange'
            self.bmi_msg = 'Obesity affects your health and well-being, you should change your diet.'
        elif self.bmi_val > 35 and self.bmi_val < 40:
            self.bmi_cat = 'Obese Class II'
            self.bmi_col = 'red'
            self.bmi_msg = 'Start playing sports and change your diet. Your obesity may cause health problems in the future.'
        elif self.bmi_val > 40:
            self.bmi_cat = 'Obese Class III'
            self.bmi_col = 'red'
            self.bmi_msg = 'You are so obese you go off the scale. Go to your doctor immediately and change your diet!'
            
    def calc_bmi(self):
        if not current_user:
            return None
        if not current_user.is_authenticated:
            return None
        profile = UserProfile.query.filter_by(id=current_user.profileId).first()
        if profile.weight and profile.height:
            return round(profile.weight / (math.pow(profile.height/100,2)),1)
        else:
            return None

from testy.models import Measurement, UserProfile
from testy.models import Dashboard as DashboardModel