import re

from starlette_admin.contrib.mongoengine import ModelView
from starlette_admin.exceptions import FormValidationError
from mongoengine.errors import NotUniqueError
from starlette_admin.fields import (
    PasswordField,
    StringField,
    BooleanField,
    EnumField,
    TextAreaField,
    IntegerField,
    DateTimeField,
)

from app.admin_panel.models import User, TGUser
from app.admin_panel.utils.auth import pwd_context
from app.admin_panel.core.config import PATTERN


class UserView(ModelView):
    row_actions = ['view', 'edit', 'delete',]
    exclude_fields_from_list = [User.password]
    exclude_fields_from_detail = [User.password]
    fields = [User.id,
              StringField('name', label='Имя'),
              StringField('login', label='Логин'),
              PasswordField('password', label='Пароль')]
    label = 'Администраторы'
    name = 'Администратор'
    fields_default_sort = [('name', True)]

    def handle_exception(self, exc):
        if isinstance(exc, NotUniqueError):
            raise FormValidationError(
                errors={
                    'login': 'Пользователь с таким логином уже существует. '
                    'Выберете другой логин'})
        return super().handle_exception(exc)

    async def before_create(self, request, data, user):
        if not re.match(PATTERN, data['password']):
            raise FormValidationError(
                errors={
                    'password': 'В пароле должно быть как минимум 8 символов, '
                    '1 заглавная буква, 1 цифра, 1 спецсимвол'})
        user.password = pwd_context.hash(data['password'])

    async def before_edit(self, request, data, user):
        new_password = user.password
        if data.get('password'):
            new_password = pwd_context.hash(data['password'])
        if not re.match(PATTERN, data['password']):
            raise FormValidationError(
                errors={
                    'password': 'В пароле должно быть как минимум 8 символов, '
                    '1 заглавная буква, 1 цифра, 1 спецсимвол'})
        user.password = new_password


class TGUserView(ModelView):
    row_actions = ['view', ]
    fields = [
        TGUser.id,
        IntegerField('tg_id', label='Телеграм ID'),
        StringField('nickname', label='Ник'),
        BooleanField('gdpr', label='Согласие'),
        BooleanField('active', label='Активность'),
    ]
    label = 'Пользователи бота'
    name = 'Пользователь бота'

    def can_create(self, request) -> bool:
        """Запретить ручное создание."""
        return False

    def can_edit(self, request) -> bool:
        """Запретить ручное изменение."""
        return False
