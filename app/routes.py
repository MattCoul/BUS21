from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task, User
from datetime import datetime
from app.forms import TaskForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash

from BUS21.app.forms import RegisterForm


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


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('User already exists!', 'error')
            return render_template('register.html', form=form)

        flash('You have successfully registered!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form)

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
