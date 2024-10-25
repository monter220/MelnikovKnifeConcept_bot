from datetime import datetime
from enum import Enum

import mongoengine as db

from .core.config import settings


class User(db.Document):
    """Модель пользователей админ панели"""
    name = db.StringField(max_length=40)
    login = db.StringField(max_length=40, required=True, unique=True)
    password = db.StringField(max_length=60, required=True)


class TGUser(db.Document):
    """Модель пользователей бота"""
    tg_id = db.IntField(required=True, unique=True)
    nickname = db.StringField(
        max_length=settings.max_len_nickname, required=True, unique=True)
    gdpr = db.BooleanField(default=False)
    active = db.BooleanField(default=True)


class TypeMessage(Enum):
    """Модель справочника типа базовых сообщений"""
    HELLO = 'hello', 'Приветствие'
    CHAT_RULES = 'chat_rules', 'Правила чата'
    CONTACT_ADMIN = 'contact_admin', 'Контакт администратора'
    UNKNOWN_COMMAND = 'unknown_command', 'Отбивка неизвестной команды'
    ABOUT = 'about', 'Описание бота'


class DefaultMessage(db.Document):
    """Модель базовых сообщений"""
    text = db.StringField(required=True)
    active = db.BooleanField(default=True)
    image = db.ImageField(help_text=settings.help_text_for_image)
    type = db.StringField(
        required=True,
        choices=[item.value for item in TypeMessage]
    )


class Message(db.Document):
    """Модель информационных сообщений"""
    text = db.StringField(required=True)
    datetime = db.DateTimeField(default=datetime.now())
    image = db.ImageField(help_text=settings.help_text_for_image)


class Knife(db.Document):
    """Модель ножей"""
    name = db.StringField(
        max_length=settings.max_len_knifename, required=True, unique=True)
    desc = db.StringField(required=True)
    previewphoto = db.ImageField(
        help_text=settings.help_text_for_image, required=True)
    photo = db.ImageField(
        help_text=settings.help_text_for_image, required=True)
