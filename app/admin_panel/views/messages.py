from starlette_admin.contrib.mongoengine import ModelView
from starlette_admin.fields import (
    PasswordField,
    StringField,
    BooleanField,
    EnumField,
    TextAreaField,
    IntegerField,
    DateTimeField,
)

from app.admin_panel.models import DefaultMessage, Message, TypeMessage


class DefaultMessageView(ModelView):
    fields = [
        DefaultMessage.id,
        DefaultMessage.image,
        TextAreaField('text', label='Текст'),
        BooleanField('active', label='Активно'),
        EnumField('type',
                  label='Тип сообщения',
                  choices=[item.value for item in TypeMessage])
    ]
    label = 'Базовые сообщения'
    name = 'Базовое сообщение'
    fields_default_sort = [
        ('type', True), ('active', True)]


class MessageView(ModelView):
    fields = [
        Message.id,
        Message.image,
        TextAreaField('text', label='Текст сообщения'),
        DateTimeField('datetime', label='Дата создания'),
    ]
    exclude_fields_from_edit = (Message.datetime, Message.id)
    exclude_fields_from_create = (Message.datetime, )
    label = 'Отправляемые сообщения'
    name = 'Отправляемое сообщение'
    fields_default_sort = [('datetime', True)]

    async def after_create(self, request, message):
        pass
