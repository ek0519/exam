from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel

from app.models import User, Social

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(session: Session, user_id):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def get_users(session: Session, offset=0, limit=10):
    return session.exec(select(User).offset(offset).limit(limit)).all()


def get_user_by_token(session: Session, token):
    statement = select(User).where(User.verify_token == token)
    results = session.exec(statement)
    return results.first()


def create(session: Session, new_model: SQLModel, callback=True):
    session.add(new_model)
    session.commit()
    if callback:
        session.refresh(new_model)
        return new_model


def reset_password(session: Session, user_id, old_password, new_password):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    print(pwd_context.verify(old_password, user.password))
    if not pwd_context.verify(old_password, user.password):
        raise HTTPException(status_code=400, detail="Password was incorrect")
    user.password = pwd_context.hash(new_password)
    user = create(session, user)
    return user


def get_social(session: Session, provider: str, provider_id: int):
    statement = select(Social) \
        .where(Social.provider == provider) \
        .where(Social.provider_id == provider_id)
    results = session.exec(statement)
    return results.first()


