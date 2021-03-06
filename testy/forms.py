from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from testy.models import User, Country
from datetime import date

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log in')

class RegisterForm(FlaskForm):

    def validate_username(self, usernameToCheck):
        user = User.query.filter_by(username=usernameToCheck.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_emailAddress(self, emailToCheck):
        emailAddress = User.query.filter_by(email=emailToCheck.data).first()
        if emailAddress:
            raise ValidationError('Email Address already exists!')

    username = StringField(label="User name", validators=[Length(min=3, max=15), DataRequired()])
    emailAddress = StringField(label=" Email address:", validators=[Email(),DataRequired()])
    password1 = PasswordField(label = "Password", validators=[Length(min=8),DataRequired()])
    password2 = PasswordField(label = "Confirm Password", validators=[EqualTo("password1",'Confirm password is different.'),DataRequired()])
    submit = SubmitField(label = "Create Account")

class ProfileForm(FlaskForm):

    def validate_date_of_birth(form, field):
        if field.data > date(2012, 1, 10):
            raise ValidationError("Enter a valid date.")

    def get_countries(self):
        countries = Country.query.all()
        choices = []
        for i, country in enumerate(countries, start=1):
            choices.append([i,country.name])
        return choices

    def get_gender(self):
        choices = [[1, 'Male'], [2,'Female']]
        return choices

    first_name = StringField(label="First name", validators=[DataRequired(message='Can\'t be blank')])
    last_name = StringField(label="Last name", validators=[DataRequired()])
    date_of_birth = DateField(label="Date of birth", validators=[DataRequired()])
    gender = SelectField(label="Gender", coerce=int, validators=[DataRequired()])
    nationality = SelectField(label="Nationality", coerce=int, validators=[DataRequired()])
    height = IntegerField(label="Height", validators=[DataRequired()])
    weight = IntegerField(label="Weight", validators=[DataRequired()])
    submit = SubmitField(label = "Save Profile")