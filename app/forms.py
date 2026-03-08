import datetime
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
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
    module = StringField("What module is it for?", validators=[DataRequired()])
    points = IntegerField("How many points is this task worth to you?", validators=[DataRequired()])
    due_date = DateField(
        "Due date:",
        format="%d-%m-%Y",
        default=date.today
    )
    submit = SubmitField("Add task")


class LoginForm(FlaskForm):
    username = StringField("What is your name?", validators=[DataRequired(), Length(max=20)])
    password = PasswordField("password", validators=[DataRequired(), Length(max=25)])
    submit = SubmitField("Sign In")

