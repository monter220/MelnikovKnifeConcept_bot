from pydantic import BaseSettings


class Settings(BaseSettings):
    app_author: str
    app_title: str
    app_doc_url: str = 'documentations'
    db_url: str = 'mongodb://localhost:27017/test_db'
    path: str
    secret: str
    admin: str
    password: str
    timezone: str = 'Europe/Moscow'
    api_version: str = 'v1'
    help_text_for_image: str = 'Название файла должно содержать только латиницу и цифры'
    max_len_nickname: int = 100
    max_len_knifename: int = 100
    pattern: str = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,}$'  # noqa


    class Config:
        env_file = '.env'


settings = Settings()
