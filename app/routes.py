from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task, User
from datetime import datetime
from app.forms import TaskForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import RegisterForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/task_display', methods=['GET', 'POST'])
def task_display():
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))

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
        query = query.order_by(Task.name.asc())
    elif order == "type":
        query = query.order_by(Task.type.asc())
    elif order == "module":
        query = query.order_by(Task.module.asc())
    elif order == "points":
        query = query.order_by(Task.points.desc())
    elif order == "due_date":
        query = query.order_by(Task.due_date.asc())

    #Show or Hide Completed tasks logic
    show_complete = request.args.get("show_complete")
    if show_complete == "False":
        query = query.filter(Task.completed == False)
    elif show_complete == "Only":
        query = query.filter(Task.completed == True)

    # Name of task filter logic
    name = request.args.get("name")
    if name:
        query = query.filter(Task.name.ilike(name))

    tasks =  query.all() # filter tasks as required

    if request.method == "POST":
        task_id = request.form.get("task_completed")
        task = Task.query.get(task_id)
        if task:
            task.completed = not task.completed
            db.session.commit()
        else:
            flash("error")
        return redirect(url_for("task_display"))

    return render_template('task_display.html', task_type=task_type, order=order, tasks=tasks, now=datetime.now(), show_complete=show_complete)

@app.route('/task_creation', methods=['GET', 'POST'])
def task_creation():
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,
                    description=form.description.data,
                    type=form.type.data,
                    module=form.module.data,
                    points=form.points.data,
                    due_date=form.due_date.data,
                    completed=False,
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
    elif request.method == 'POST':
        flash(f"Task not valid.")
    return render_template('task_creation.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
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
    if 'user_id' not in session:
        flash(f'You are already logged out - please login')
        return redirect(url_for('login'))
    else:
        username = session.get('username')
        session.clear()
        flash(f'{username} you have been logged out')
        return redirect(url_for('login'))

@app.route('/view_points')
def view_points():
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))
    else:
        query = Task.query
        points = query.all()
        points_total = db.session.query(
            func.sum(Task.points)
        ).all()
        print(points_total)
    return render_template('view_points.html', points=points, points_total=points_total)

@app.route('/points_goal')
def points_goal():
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))
    else:
        pass

@app.route('/deleting/<int:task_id>', methods=['GET', 'POST'])
def deleting_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('index'))


@app.route('/updating/<int:task_id>', methods=['GET', 'POST'])
def updating_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('index'))

    return render_template('task_updating.html', form=form, task=task)