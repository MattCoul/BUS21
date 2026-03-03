from flask import render_template, redirect, url_for, flash, request
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/task_display')
def task_display():
    query = Task.query

    # Type of tasks display logic
    task_type = request.args.get("task_type")
    if task_type == "exam":
        query = query.filter(Task.task == "exam")
    elif task_type == "groupProject":
        query = query.filter(Task.task == "groupProject")
    elif task_type == "coursework":
        query = query.filter(Task.task == "coursework")
    elif task_type == "customTasks":
        query = query.filter(Task.task == "customTasks")

    # Order of displayed tasks logic
    order = request.args.get("order")
    if order == "name":
        query = query.order_by(Task.name.desc())
    elif order == "type":
        query = query.order_by(Task.type.desc())
    elif order == "module":
        query = query.order_by(Task.module.desc())
    elif order == "points":
        query = query.order_by(Task.points.desc())
    elif order == "due_date":
        query = query.order_by(Task.due_date.desc())

    # tasks =  query.all() # To be used one task creation set up
    tasks = [] # Dummy until task creation is set up

    return render_template('task_display.html', task_type=task_type, order=order, tasks=tasks, now=datetime.now())

@app.route('/task_creation')
def task_creation():
    return render_template('task_creation.html')

@app.route('/login')
def login():
    return render_template('login.html')