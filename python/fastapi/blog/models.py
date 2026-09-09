from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default=None
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
