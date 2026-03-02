from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime, timezone

# The base class database model
class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    module: so.Mapped[str] = so.mapped_column(sa.String(256))
    points: so.Mapped[int] = so.mapped_column(nullable=False)
    due_date: so.Mapped[str] = so.mapped_column(sa.DATE, nullable=False, default=lambda: datetime.now(timezone.utc))