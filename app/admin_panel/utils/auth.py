from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed
from app.admin_panel.models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class MyAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        user = User.objects(login=username).first()
        if user and pwd_context.verify(password, user.password):
            request.session.update({'username': username})
            return response
        raise LoginFailed('Неверное имя пользователя или пароль.')

    async def is_authenticated(self, request) -> bool:
        user = User.objects(
            login=request.session.get('username', None)).first()
        if user:
            request.state.user = user
            return True
        return False

    async def logout(
            self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
