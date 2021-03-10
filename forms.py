from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class NewUserForm(FlaskForm):
    username = StringField("Username", 
                            validators=[InputRequired(
                                message="You need a username to go by!")])
    password = StringField("Password")
    email = StringField("email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Enter username")])
    password = StringField("Password", validators=[InputRequired(message="Enter password")])

class AddFeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Enter a title")])
    content = StringField("Content", validators=[InputRequired(message="Enter content")])

class EditFeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Enter a title")])
    content = StringField("Content", validators=[InputRequired(message="Enter content")])