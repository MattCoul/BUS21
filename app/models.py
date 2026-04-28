from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime, timezone

user_modules = db.Table('user_modules',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('module_id', db.Integer, db.ForeignKey('module.id')))

class UserTasks(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('task.id'))
    completed: so.Mapped[bool] = so.mapped_column(default=False, nullable=False)
    user: so.Mapped["User"] = so.relationship(back_populates="user_tasks")
    task: so.Mapped["Task"] = so.relationship(back_populates="user_tasks")

# The base class database model
class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    type: so.Mapped[str] = so.mapped_column(sa.String(265), default="Custom")
    points: so.Mapped[int] = so.mapped_column(nullable=False)
    due_date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, default=lambda: datetime.now(timezone.utc))
    module_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('module.id'), nullable=False)
    module: so.Mapped["Module"] = so.relationship('Module', back_populates="tasks")
    user_tasks: so.Mapped[list["UserTasks"]] = so.relationship("UserTasks", back_populates="task")

#base user db
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    user_tasks: so.Mapped[list["UserTasks"]] = so.relationship("UserTasks", back_populates="user")
    modules: so.Mapped[list["Module"]] = so.relationship('Module', secondary="user_modules", back_populates='users')

class Goal(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    goal: so.Mapped[int] = so.mapped_column(nullable=False, default=0)

class Module(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    module_name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    tasks: so.Mapped[list["Task"]] = so.relationship('Task', back_populates="module")
    users: so.Mapped[list["User"]] = so.relationship('User', secondary="user_modules", back_populates='modules')