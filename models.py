from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from passlib.apps import custom_app_context
from flask_login import UserMixin

from db import engine

class Base(DeclarativeBase):
  pass

class User(Base, UserMixin):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(30), unique=True)
  password: Mapped[str] = mapped_column(String(256))

  def hash_password(self):
    self.password = custom_app_context.encrypt(self.password)

  def verify_password(self, password) -> bool:
    return custom_app_context.verify(password, self.password)

  def __repr__(self) -> str:
    return f"User(id={self.id}, username={self.username})"

  def to_dict(self) -> dict:
    return { 'id': self.id, 'username': self.username }

class ShortLink(Base):
  __tablename__ = "shortlinks"

  id: Mapped[int] = mapped_column(primary_key=True)
  kind: Mapped[str] = mapped_column(String(9))
  short: Mapped[str] = mapped_column(String(12))
  alias: Mapped[Optional[str]] = mapped_column(String(12), unique=True, nullable=True)
  redirects_count: Mapped[int] = mapped_column(default=0)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

  @validates("kind")
  def validate_kind(self, key, kind):
    if not kind in ["public", "protected", "private"]:
      raise ValueError("Kind must be in [public, protected, private]")

    return kind

  def __repr__(self) -> str:
    return f"Shortlink(id={self.id}, kind={self.kind}, short={self.short}, alias={self.alias}, redirects_count={self.redirects_count}), user_id={self.user_id}"

  def to_dict(self) -> dict:
    return { 'id': self.id, 'kind': self.kind, 'short': self.short, 'alias': self.alias, 'redirects_count': self.redirects_count, 'user_id': self.user_id }

Base.metadata.create_all(engine)