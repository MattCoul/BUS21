import datetime
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    name = StringField("What do you want to call the task?", validators=[DataRequired()])
    description = StringField("What do you have to do?", validators=[DataRequired()])
    type = SelectField(
        "Select the task type:",
        choices = [("exam", "Exam"),
                   ("groupProject", "Group Project"),
                   ("coursework", "Coursework"),
                   ("customTasks", "Custom")],
        validators=[DataRequired()]
    )
    module = SelectField(
        "Select the task module:",
        choices = [("SWW1", "SWW1"),
                   ("SWW2", "SWW2"),
                   ("BUS", "BUS"),
                   ("AIML", "AIML"),
                   ("CS", "CS"),
                   ("DSAD", "DSAD"),
                   ("other", "Other")],
        validators=[DataRequired()]
    )
    points = IntegerField("How many points is this task worth to you?", validators=[DataRequired()])
    due_date = DateField(
        "Due date:",
        format="%Y-%m-%d",
        default=date.today,
        validators=[DataRequired()]
    )
    submit = SubmitField("Add task")


class LoginForm(FlaskForm):
    username = StringField("Username?", validators=[DataRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=25)])
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Register")

class PointsForm(FlaskForm):
    goal = IntegerField("How many points do you want to want to earn?", validators=[DataRequired()])
    submit = SubmitField("Set Points Goal")