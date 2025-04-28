import base64
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from models import DefaultMessage, Message
from schemas import DefaultMessageBase, MessageBase, MessageStatusUpdated, MessageStatusUpdate


router_defaultmessage = APIRouter()
router_delayedmessage = APIRouter()


@router_defaultmessage.get('/{message_type}', response_model=DefaultMessageBase)
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


@router_delayedmessage.get('/{message_id}', response_model=MessageBase)
async def get_delayed_messages(message_id: str):
    delayed_message = Message.objects(id=message_id).first()
    if not delayed_message:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Сообщение с id {message_id} не найдено.')
    image = delayed_message.image.read()
    if image:
        image_base64 = base64.b64encode(image).decode('utf-8')
    else:
        image_base64 = None
    response_data = {
        'text': delayed_message.text,
        'image': image_base64,
        'id_celery': delayed_message.id_celery,
        'status': delayed_message.status
    }
    return response_data


@router_delayedmessage.patch(
        '/{message_id}/status',
        response_model=MessageStatusUpdated
)
async def update_status(message_id: str, update: MessageStatusUpdate):
    delayed_message = Message.objects(id=message_id).first()
    if not delayed_message:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Сообщение с {message_id} не найдено.')
    delayed_message.status = update.status
    delayed_message.save()

    return delayed_message
