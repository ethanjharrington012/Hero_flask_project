from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    # email, password, submit_buttom
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit_buttom = SubmitField()

class HeroForm(FlaskForm):
    name = StringField('name')
    description = StringField('description')
    comic_in = IntegerField('Comic in')
    super_power = StringField('Super power')
    random_quote = StringField('Random quote')
    submit_button = SubmitField()