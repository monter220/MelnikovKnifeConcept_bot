from typing import Optional

from pydantic import BaseModel, Field


class DefaultMessageBase(BaseModel):
    text: str = Field(..., description='Текст сообщения')
    type: str = Field(..., description='Тип сообщения')
    image: Optional[str] = Field(
        None,
        description='Изображение')
