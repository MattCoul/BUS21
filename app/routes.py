from flask import render_template, redirect, url_for, flash, request
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def task_display():
    query = Task
    taskType = request.args.get("task_type")
    order = request.args.get("order")

    return render_template('task_display', task_type=task_type, )