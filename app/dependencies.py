from fastapi import Request, HTTPException


async def get_auth_cookie(request: Request):
    if request.session.get('user_id') is None:
        raise HTTPException(status_code=401, detail='No Authorization cookie')


async def is_verify(request: Request):
    if request.session.get('is_verify') is not True:
        raise HTTPException(status_code=400, detail='User was not verified')
