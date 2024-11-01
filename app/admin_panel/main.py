import uvicorn
from fastapi import FastAPI
from starlette_admin.contrib.mongoengine import Admin
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from .utils.auth import MyAuthProvider, pwd_context
from starlette_admin.i18n import I18nConfig
from mongoengine import connect, disconnect

from app.admin_panel.models import User, DefaultMessage, TGUser, Knife, Message
from .views import UserView, TGUserView, DefaultMessageView, MessageView, KnifeView
from .core.config import DB_URL, ADMIN, PASSWORD, APP_TITLE, APP_DOC_URL, APP_ADMIN_PANEL_URL, SECRET


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect(host=DB_URL)
    if not User.objects(login=ADMIN):
        user = User(
            login=ADMIN,
            password=pwd_context.hash(PASSWORD)
        )
        user.save()
    yield
    disconnect()


app = FastAPI(
    lifespan=lifespan,
    title=APP_TITLE,
    docs_url=APP_DOC_URL,
    redoc_url=None,
)


admin = Admin(
    title=APP_TITLE,
    base_url=APP_ADMIN_PANEL_URL,
    auth_provider=MyAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET)],
    i18n_config=I18nConfig(default_locale='ru'),
)


admin.add_view(UserView(User))
admin.add_view(KnifeView(Knife))
admin.add_view(DefaultMessageView(DefaultMessage))
admin.add_view(TGUserView(TGUser))
admin.add_view(MessageView(Message))

admin.mount_to(app)

if __name__ == '__main__':
    uvicorn.run('main:app',
                reload=True,
                port=9000,
                host='localhost',
                forwarded_allow_ips='*')
