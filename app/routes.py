from flask import render_template, redirect, url_for, flash, request
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task
from datetime import datetime
from app.forms import TaskForm

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/task_display')
def task_display():
    query = Task.query

    # Type of tasks display logic
    task_type = request.args.get("task_type")
    if task_type == "exam":
        query = query.filter(Task.type == "exam")
    elif task_type == "groupProject":
        query = query.filter(Task.type == "groupProject")
    elif task_type == "coursework":
        query = query.filter(Task.type == "coursework")
    elif task_type == "customTasks":
        query = query.filter(Task.type == "customTasks")

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

    # Name of task filter logic
    name = request.args.get("name")
    if name:
        query = query.filter(Task.name.ilike(name))

    # tasks =  query.all() # To be used one task creation set up
    tasks = [] # Dummy until task creation is set up

    return render_template('task_display.html', task_type=task_type, order=order, tasks=tasks, now=datetime.now())

@app.route('/task_creation', methods=['GET', 'POST'])
def task_creation():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,
                    description=form.description.data,
                    type=form.type.data,
                    module=form.module.data,
                    points=form.points.data,
                    due_date=form.due_date.data,
                    )
        try:
            db.session.add(task)
            db.session.commit()
            flash(f"Task successfully added.")
            return redirect(url_for('task_creation'))
        except IntegrityError:
            db.session.rollback()
            flash(f"This task cannot be created.")
            return redirect(url_for('task_creation'))
    else:
        flash(f"Task not valid.")
    return render_template('task_creation.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('login.html', username=session['username'])

    if request.method == 'POST' and 'username' not in session:
        username = request.form.get('username')
        if username:
            session['username'] = username
            flash(f"Login successful for {username} - Welcome")
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' not in session:
        flash(f'You are already logged out - please login')
        return redirect(url_for('login'))
    else:
        username = session.get('username')
        session.clear()
        flash(f'{username} you have been logged out')
        return redirect(url_for('login'))
