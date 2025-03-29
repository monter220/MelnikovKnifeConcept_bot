from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, SecretStr


class BotConfig(BaseModel):
    """Модель параметров бота."""

    telegram_token: SecretStr
    parse_mode: str = ParseMode.HTML
    fastapi_url: str
    debug: bool = False


class Settings(BaseSettings):
    """Основные настройки бота."""

    bot: BotConfig

    model_config = SettingsConfigDict(
        env_file='.env', env_nested_delimiter='__', extra='ignore'
    )


settings = Settings()
