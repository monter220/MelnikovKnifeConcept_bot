from starlette_admin.contrib.mongoengine import ModelView
from starlette_admin.exceptions import FormValidationError
from mongoengine.errors import NotUniqueError
from starlette_admin.fields import (
    StringField,
    BooleanField,
    TextAreaField,
    IntegerField,
)

from models import Knife


class KnifeView(ModelView):
    fields = [
        Knife.id,
        StringField(
            'name',
            label='Название',
            help_text='Укажите уникальное название ножа',
        ),
        TextAreaField('desc', label='Описание ножа'),
        # Knife.previewphoto,
        Knife.photo,
        IntegerField('weight', label='Вес ножа в граммах'),
        IntegerField('length', label='Длина ножа в миллиметрах'),
        IntegerField('width', label='Ширина ножа в миллиметрах'),
        IntegerField('thickness', label='Толщина ножа в миллиметрах'),
        TextAreaField('features', label='Особенности ножа'),
        StringField(
            'pretentious_quote',
            label='Цитата',
            help_text='Пафосная цитата',
        ),
        BooleanField(
            'active',
            label='Активен',
            help_text='Признак доступности ножа для отправки пользователям',
        )
    ]
    label = 'Ножи'
    name = 'Нож'
    fields_default_sort = [
        ('active', True), ('name', True)]

    def handle_exception(self, exc):
        if isinstance(exc, NotUniqueError):
            error_message = str(exc)
            errors = {}
            if 'name' in error_message:
                errors['name'] = 'Нож с таким названием уже существует.'
            if errors:
                raise FormValidationError(errors=errors)
        return super().handle_exception(exc)
