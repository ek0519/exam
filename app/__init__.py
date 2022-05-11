from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


def create_app():
    app = FastAPI(title="Exam API",
                  description="Exam API",
                  docs_url="/api/docs",
                  redoc_url="/api/redoc",
                  openapi_url="/api/openapi.json")
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    origins = [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "https://127.0.0.1:3000",
        "http://localhost:3000",
        "https://localhost:3000",
        "https://exam.servants.me",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SessionMiddleware,
                       secret_key='example', same_site='None', https_only=True)

    from app.routers import auth, user

    app.include_router(prefix='/api', router=auth.router)
    app.include_router(prefix='/api', router=user.router)
    return app
