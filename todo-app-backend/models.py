from uuid import uuid4

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
