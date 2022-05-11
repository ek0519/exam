from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session

from app import crud
from app.dependencies import is_verify, get_auth_cookie
from app.main import get_session
from app.schema import UserList, UserResetPassword, ChangeUserName

router = APIRouter(dependencies=[Depends(is_verify), Depends(get_auth_cookie)])


@router.get("/users",
            response_model=List[UserList])
def get_users(offset: int = 0, limit: int = 10,
              session: Session = Depends(get_session)
              ):
    users = crud.get_users(session, offset=offset, limit=limit)
    if not users:
        return []
    return users


@router.get("/users/{user_id}", response_model=UserList)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    return user


@router.patch("/users/password", response_model=UserList)
def change_password(request: Request, user: UserResetPassword,
                    session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if user_id:
        user = crud.reset_password(
            session, user_id, user.old_password, user.new_password)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.patch("/users", response_model=UserList)
def change_name(request: Request, user: ChangeUserName,
                session: Session = Depends(get_session)):
    user_id = request.session.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    current_user = crud.get_user(session, user_id)
    current_user.name = user.name
    current_user = crud.create(session, current_user)
    return current_user
