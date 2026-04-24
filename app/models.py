from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime, timezone

# The base class database model
class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    type: so.Mapped[str] = so.mapped_column(sa.String(265), default="Custom")
    points: so.Mapped[int] = so.mapped_column(nullable=False)
    due_date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed: so.Mapped[bool] = so.mapped_column(default=False)
    module_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('module.id'), nullable=False)
    module: so.Mapped["Module"] = so.relationship(back_populates="tasks")

#base user db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Integer, nullable=False, default=0)

class Module(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    module_name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    tasks: so.Mapped[list["Task"]] = so.relationship(back_populates="module")