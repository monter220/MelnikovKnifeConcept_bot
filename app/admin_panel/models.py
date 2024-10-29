from datetime import datetime
from enum import Enum

import mongoengine as db

from .core.config import (
    HELP_TEXT_FOR_IMAGE,
    MAX_LEN_KNIFENAME,
    MAX_LEN_NICKNAME,
    MAX_LEN_KNIFEQUOTE,
    MIN_KNIFE_VAL,
    MAX_KNIFE_VAL,
    MAX_KNIFE_THICKNESS,
    HELP_TEXT_FOR_KNIFE_LENGTH,
    HELP_TEXT_FOR_KNIFE_WEIGHT,
)


class User(db.Document):
    """Модель пользователей админ панели"""
    name = db.StringField(max_length=40)
    login = db.StringField(max_length=40, required=True, unique=True)
    password = db.StringField(max_length=60, required=True)


class TGUser(db.Document):
    """Модель пользователей бота"""
    tg_id = db.IntField(required=True, unique=True)
    nickname = db.StringField(
        max_length=MAX_LEN_NICKNAME, required=True, unique=True)
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
    image = db.ImageField(help_text=HELP_TEXT_FOR_IMAGE)
    type = db.StringField(
        required=True,
        choices=[item.value for item in TypeMessage]
    )


class Message(db.Document):
    """Модель информационных сообщений"""
    text = db.StringField(required=True)
    datetime = db.DateTimeField(default=datetime.now())
    image = db.ImageField(help_text=HELP_TEXT_FOR_IMAGE)


class Knife(db.Document):
    """Модель ножей"""
    name = db.StringField(
        max_length=MAX_LEN_KNIFENAME, required=True, unique=True)
    desc = db.StringField(required=True)
    previewphoto = db.ImageField(
        help_text=HELP_TEXT_FOR_IMAGE, required=True)
    photo = db.ImageField(
        help_text=HELP_TEXT_FOR_IMAGE, required=True)
    weight = db.IntField(
        required=True,
        min_value=MIN_KNIFE_VAL,
        max_value=MAX_KNIFE_VAL,
        help_text=HELP_TEXT_FOR_KNIFE_WEIGHT,
    )
    length = db.IntField(
        required=True,
        min_value=MIN_KNIFE_VAL,
        max_value=MAX_KNIFE_VAL,
        help_text=HELP_TEXT_FOR_KNIFE_LENGTH,
    )
    width = db.IntField(
        required=True,
        min_value=MIN_KNIFE_VAL,
        max_value=MAX_KNIFE_VAL,
        help_text=HELP_TEXT_FOR_KNIFE_LENGTH,
    )
    thickness = db.IntField(
        required=True,
        min_value=MIN_KNIFE_VAL,
        max_value=MAX_KNIFE_THICKNESS,
        help_text=HELP_TEXT_FOR_KNIFE_LENGTH,
    )
    features = db.StringField()
    pretentious_quote = db.StringField(
        max_length=MAX_LEN_KNIFEQUOTE, required=True, unique=True)
