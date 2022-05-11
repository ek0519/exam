from datetime import datetime
from typing import Optional, List, Dict, Any

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint, Column
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('email'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_login_at: datetime = Field(default=None, nullable=True)
    name: str
    email: str
    remember_me: Optional[str]
    password: str
    is_verify: bool = Field(default=False, nullable=False)
    verify_token: Optional[str] = None
    login_time: Optional[int] = Field(default=0, nullable=True)
    last_login_ip: Optional[str] = Field(str)
    socials: List["Social"] = Relationship(back_populates='user')


class Social(SQLModel, table=True):
    __tablename__ = 'socials'
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    provider: str = Field(..., nullable=False)
    provider_id: str = Field(..., nullable=False)
    raw_data: Dict[Any, Any] = Field(..., nullable=False, sa_column=Column(sa.JSON))
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional[User] = Relationship(back_populates="socials")




