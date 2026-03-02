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
    query = Task
    task_type = request.args.get("task_type")
    order = request.args.get("order")
    tasks = []
    return render_template('task_display.html', task_type=task_type, order=order, tasks=tasks, now=datetime.now())