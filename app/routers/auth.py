import uuid
from datetime import datetime

import httpx
from fastapi import APIRouter, Request, Response, Depends, Body, HTTPException, BackgroundTasks, Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app import crud
from app.crud import get_user_by_token, pwd_context
from app.dependencies import get_auth_cookie
from app.main import get_session
from app.models import User, Social
from app.schema import UserOut, CreateUser, FacebookAuth
from app.services.mail import simple_send
from config import settings

router = APIRouter(prefix='/auth')


@router.get('/me', response_model=UserOut)
async def check_auth(request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        raise HTTPException(status_code=403, detail='User not logged in')
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


@router.post('/verify', dependencies=[Depends(get_auth_cookie)])
async def verify_email(request: Request,
                       background_tasks: BackgroundTasks,
                       session: Session = Depends(get_session)):
    user_id = request.session.get('user_id', None)
    user = crud.get_user(session, user_id)
    if user.is_verify is True:
        raise HTTPException(status_code=400, detail='User already verified')
    title = 'Please verify your email'
    background_tasks.add_task(simple_send,
                              title, [user.email], user.verify_token)
    return {'message': 'Verification email sent'}


@router.post('/signup', response_model=UserOut)
async def sign_up(request: Request,
                  background_tasks: BackgroundTasks,
                  session: Session = Depends(get_session),
                  user: CreateUser = Body(...)):
    client_host = request.client.host
    hash_password = pwd_context.hash(user.password)
    token = str(uuid.uuid4())
    request.session['signup_token'] = token
    new_user = User(name=user.name, email=user.email, password=hash_password,
                    last_login_ip=client_host, verify_token=token)
    try:
        crud.create(session, new_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail='User already exists')
    title = 'Please verify your email'
    background_tasks.add_task(simple_send, title, [new_user.email], token)
    return new_user


@router.get('/logout')
def logout(request: Request, response: Response):
    request.session.clear()
    response.delete_cookie('Authorization')
    return {}


@router.get('/verify/{token}', response_model=UserOut)
def verify_token(token: str, request: Request,
                 session: Session = Depends(get_session)
                 ):
    client_host = request.client.host
    user = get_user_by_token(session, token)
    if not user:
        raise HTTPException(status_code=400, detail='Token is invalid')
    user.is_verify = True
    user.verify_token = None
    user.remember_me = str(uuid.uuid4())
    user.last_login_at = datetime.now()
    user.last_login_ip = client_host
    crud.create(session, user)
    request.session['user_id'] = user.id
    request.session['is_verify'] = user.is_verify
    return RedirectResponse(settings.APP_URL)


@router.post('/login', response_model=UserOut)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session),
          ):
    client_host = request.client.host
    user_id = request.session.get('user_id', None)
    if user_id is None:
        statement = select(User).where(User.email == form_data.username)
        results = session.exec(statement)
        user_data = results.first()
        if user_data is None:
            raise HTTPException(
                status_code=400, detail='User not found')
        if not pwd_context.verify(
                form_data.password,
                user_data.password):
            raise HTTPException(status_code=400, detail='User or Password is incorrect')
        user_data.login_time += 1
        user_data.remember_me = str(uuid.uuid4())
        user_data.last_login_at = datetime.now()
        user_data.last_login_ip = client_host
        user_data = crud.create(session, user_data)
    else:
        user_data = crud.get_user(session, user_id)
    request.session['user_id'] = user_data.id
    request.session['is_verify'] = user_data.is_verify
    return user_data


@router.post('/google', response_class=RedirectResponse)
def google_login(request: Request,
                 response: Response,
                 credential: str = Form(...),
                 session: Session = Depends(get_session)):
    client_host = request.client.host

    google_oauth2_api = 'https://oauth2.googleapis.com/tokeninfo'
    res = httpx.get(google_oauth2_api, params={'id_token': credential})
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail='Google login error')
    data = res.json()
    statement = select(User).where(User.email == data['email'])
    user = session.exec(statement).first()
    if user:
        user.login_time += 1
        user.is_verify = True
        user.last_login_ip = client_host
        user.verify_token = None
        user.remember_me = str(uuid.uuid4())
        user.last_login_at = datetime.now()
        user.last_login_ip = client_host
        user = crud.create(session, user)
    else:
        user = User(name=data['name'],
                    email=data['email'],
                    password=pwd_context.hash(str(uuid.uuid4())),
                    last_login_ip=client_host,
                    is_verify=True,
                    remember_me=str(uuid.uuid4()),
                    login_time=1,
                    last_login_at=datetime.now())
        user = crud.create(session, user)

    social = crud.get_social(session, 'google', data['sub'])
    if social:
        pass
    else:
        social = Social(user_id=user.id, provider='google',
                        provider_id=data['sub'], raw_data=data)
        crud.create(session, social, callback=False)

    request.session['user_id'] = user.id
    request.session['is_verify'] = user.is_verify
    response.status_code = 302
    return settings.APP_URL


@router.post('/facebook', response_model=UserOut)
def facebook_login(request: Request, auth: FacebookAuth,
                   session: Session = Depends(get_session)
                   ):
    client_host = request.client.host
    user_id = request.session.get('user_id', None)
    if user_id:
        user = crud.get_user(session, user_id)
    else:
        facebook_graph_api = 'https://graph.facebook.com/v13.0/me'
        res = httpx.get(facebook_graph_api, params={'access_token': auth.access_token, 'fields': 'id,name,email'})
        data = res.json()
        statement = select(User).where(User.email == data['email'])
        user = session.exec(statement).first()
        if user:
            user.login_time += 1
            user.is_verify = True
            user.last_login_ip = client_host
            user.verify_token = None
            user.remember_me = str(uuid.uuid4())
            user.last_login_at = datetime.now()
            user = crud.create(session, user)

        else:
            user = User(name=data['name'], email=data['email'],
                        password=pwd_context.hash(str(uuid.uuid4())),
                        last_login_ip=client_host,
                        is_verify=True,
                        remember_me=str(uuid.uuid4()),
                        login_time=1,
                        last_login_at=datetime.now())
            user = crud.create(session, user)

        social = crud.get_social(session, 'facebook', data['id'])
        if not social:
            social = Social(user_id=user.id, provider='facebook',
                            provider_id=data['id'], raw_data=data)
            crud.create(session, social, callback=False)

    request.session['user_id'] = user.id
    request.session['is_verify'] = user.is_verify
    return user
