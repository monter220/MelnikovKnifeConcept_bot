from starlette_admin.contrib.mongoengine import ModelView
from starlette_admin.fields import (
    BooleanField,
    EnumField,
    TextAreaField,
    DateTimeField,
    StringField,
)

from models import DefaultMessage, Message, TypeMessage
from utils import validate_datetime_field, create_task, delete_task


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
        DateTimeField('datetime', label='Дата отправки'),
        StringField('id_celery', label='ID планировщика'),
        BooleanField('status', label='Состояние'),
    ]
    exclude_fields_from_edit = (Message.status,
                                Message.id_celery)
    exclude_fields_from_create = (Message.status,
                                  Message.id_celery)
    label = 'Отправляемые сообщения'
    name = 'Отправляемое сообщение'
    fields_default_sort = [('datetime', True)]

    async def before_create(self, request, data, message):
        validate_datetime_field(data=data, obj=message)

    async def before_edit(self, request, data, message):
        validate_datetime_field(data=data, obj=message)

    async def after_create(self, request, message):
        create_task(message=message)

    async def after_edit(self, request, message):
        delete_task(message=message)
        create_task(message=message)

    async def after_delete(self, request, message):
        delete_task(message=message)
