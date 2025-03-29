from pydantic import BaseModel, Field


class PreviewKnifeList(BaseModel):
    name: str = Field(..., description='Название ножа')
    # previewphoto: str = Field(
    #     None, description='Предпросмотровое изображение ножа')


class KnifeBase(BaseModel):
    name: str = Field(..., description='Название ножа')
    desc: str = Field(..., description='Описание ножа')
    photo: str = Field(
        None, description='Красивое изображение ножа')
    weight: int = Field(..., description='Вес ножа в гр')
    length: int = Field(..., description='Длина ножа в мм')
    width: int = Field(..., description='Ширина ножа в мм')
    thickness: int = Field(..., description='Толщина ножа в мм')
    features: str = Field(..., description='Особенности ножа')
    pretentious_quote: str = Field(..., description='Пафосная цитата')
