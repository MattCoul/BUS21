from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models import Task, User, Goal, Module, UserTasks
from datetime import datetime
from app.forms import create_task_form, LoginForm, PointsForm
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

    user_id = session['user_id']
    query = db.session.query(Task, UserTasks.completed).join(UserTasks, Task.id == UserTasks.task_id).filter(UserTasks.user_id == user_id)

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
        query = query.join(Module).order_by(Module.module_name.asc())
    elif order == "points":
        query = query.order_by(Task.points.desc())
    elif order == "due_date":
        query = query.order_by(Task.due_date.asc())

    #Show or Hide Completed tasks logic
    show_complete = request.args.get("show_complete")
    if show_complete == "False":
        query = query.filter(UserTasks.completed == False)
    elif show_complete == "Only":
        query = query.filter(UserTasks.completed == True)

    # Name of task filter logic
    name = request.args.get("name")
    if name:
        query = query.filter(Task.name.ilike(name))

    tasks =  query.all() # filter tasks as required

    if request.method == "POST":
        task_id = request.form.get("task_completed")
        task = UserTasks.query.filter_by(user_id=session['user_id'], task_id=task_id).first()
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
    all_modules = Module.query.all()
    modules_list = []
    print(all_modules)
    for m in all_modules:
        modules_list.append((m.id, m.module_name))
    form = create_task_form(modules_list=modules_list)()
    if form.validate_on_submit():
        module_id = form.module.data
        task = Task(name=form.name.data,
                    description=form.description.data,
                    type=form.type.data,
                    module_id=module_id,
                    points=form.points.data,
                    due_date=form.due_date.data
                    )
        try:
            db.session.add(task)
            db.session.commit()
            user_task = UserTasks(user_id=session['user_id'], task_id=task.id)
            db.session.add(user_task)
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
    if 'user_id' not in session:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        flash(f'You are already logged in.')
        return redirect(url_for('task_display'))
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
        points_total = points_total[0][0]

    goal = Goal.query.order_by(Goal.id.desc()).all()
    goal1 = goal[0].goal

    return render_template('view_points.html', points=points, points_total=points_total, goal=goal1)

@app.route('/points_goal', methods=['GET', 'POST'])
def points_goal():
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))
    else:
        form = PointsForm()
        if form.validate_on_submit():
            try:
                goal = Goal(goal=form.goal.data)
                db.session.add(goal)
                db.session.commit()
                flash(f"Point goal successfully updated.")
                return redirect(url_for('view_points'))
            except IntegrityError:
                db.session.rollback()
                flash(f"Error! Looks like this goal cannot be set. Try again")
                return render_template('points_goal.html',
                                       form=form)
    goal = Goal.query.all()
    return render_template('points_goal.html', form=form, goal=goal)


@app.route('/modules')
def modules():
    module_data = Module.query.all()
    return render_template('modules.html', modules_list = module_data)

@app.route('/module_add/<int:module_id>', methods=['POST'])
def module_add(module_id):
    if "user_id" not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))
    user_id = session['user_id']
    module = Module.query.get_or_404(module_id)
    tasks = Task.query.filter_by(module_id=module.id).all()
    for task in tasks:
        is_new = UserTasks.query.filter_by(user_id=user_id, task_id=task.id).first()
        if not is_new:
            db.session.add(UserTasks(user_id=user_id, task_id=task.id, completed=False))
    db.session.commit()
    flash('All module tasks added to your list!')
    return redirect(url_for('modules'))

  
@app.route('/deleting/<int:task_id>', methods=['GET', 'POST'])
def deleting_task(task_id):
    UserTasks.query.filter_by(user_id=session['user_id'], task_id=task_id).delete()
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('task_display'))


@app.route('/updating/<int:task_id>', methods=['GET', 'POST'])
def updating_task(task_id):
    task = Task.query.get_or_404(task_id)
    modules_list = [(m.id, m.module_name) for m in Module.query.all()]
    TaskForm = create_task_form(modules_list=modules_list)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.type = form.type.data
        task.module_id = form.module.data
        task.points = form.points.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('task_display'))

    return render_template('task_updating.html', form=form, task=task)

@app.route("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    return redirect(request.referrer)