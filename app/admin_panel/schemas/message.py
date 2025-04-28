from typing import Optional

from pydantic import BaseModel, Field


class DefaultMessageBase(BaseModel):
    text: str = Field(..., description='Текст сообщения')
    type: str = Field(..., description='Тип сообщения')
    image: Optional[str] = Field(
        None,
        description='Изображение')


class MessageBase(BaseModel):
    text: str = Field(..., description='Текст сообщения')
    image: Optional[str] = Field(
        None,
        description='Изображение')
    id_celery: Optional[str] = Field(
        None,
        description='ID задачи в Celery')
    status: bool = Field(
        default=False,
        description='Состояние сообщения (отправлено/не отправлено)')


class MessageStatusUpdate(BaseModel):
    status: bool = Field(
        ...,
        description='Состояние сообщения (отправлено/не отправлено)')


class MessageStatusUpdated(BaseModel):
    text: str = Field(..., description='Текст сообщения')
    id_celery: Optional[str] = Field(
        None,
        description='ID задачи в Celery')
    status: bool = Field(
        default=False,
        description='Состояние сообщения (отправлено/не отправлено)')
