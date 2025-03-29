import base64
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from models import DefaultMessage
from schemas import DefaultMessageBase


router = APIRouter()


@router.get('/{message_type}', response_model=DefaultMessageBase)
async def get_default_messages(message_type: str):
    message = DefaultMessage.objects(type=message_type, active=True).first()
    if not message:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Сообщение с типом {message_type} не найдено.')
    image = message.image.read()
    if image:
        image_base64 = base64.b64encode(image).decode('utf-8')
    else:
        image_base64 = None
    response_data = {
        'text': message.text,
        'image': image_base64,
        'type': message.type,
    }
    return response_data
