from pydantic import BaseModel, Field


class TGUserBase(BaseModel):
    tg_id: int = Field(..., description='Telegram ID пользователя')
    nickname: str = Field(
        ...,
        description='Никнейм пользователя')
    gdpr: bool = Field(
        default=False,
        description='Согласие на обработку данных')
    active: bool = Field(
        default=True,
        description='Статус активности пользователя')


class TGUsersList(BaseModel):
    tg_id: int = Field(..., description='Telegram ID пользователя')
