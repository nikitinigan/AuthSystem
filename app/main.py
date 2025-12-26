from fastapi import FastAPI
from app.users.router import router_auth
from app.users.router import router_users
from app.mock.router import router_mock


app = FastAPI(
    title="Система аутентификации и авторизации",
)

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_mock)