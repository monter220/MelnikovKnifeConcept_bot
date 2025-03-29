from http import HTTPStatus

from aiohttp import ClientResponseError
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.methods import SendMessage

from constants import MessagesConstants, TypesDefaultMessages
from keyboards import (confirm_gdpr_keyboard, main_keyboard,
                       back_keyboard, get_form_keyboard, back_button, knifes_button)
from utils import (get_tg_user, create_tg_user,
                   get_default_message,
                   make_image_from_base64,
                   get_knifes, get_single_knife)


router = Router()


@router.message(Command('start'))
async def start_handler(message: Message) -> SendMessage:
    """Приветствуем пользователя.
    Предлагаем приянть соглашение.
    """
    if not message.from_user.username:
        return await message.answer(MessagesConstants.NO_USERNAME)

    try:
        await get_tg_user(message.from_user.id)
        return await message.answer(
            MessagesConstants.MAIN, reply_markup=main_keyboard)
    except ClientResponseError as e:
        if e.status == HTTPStatus.NOT_FOUND:
            hello_message = await get_default_message(
                TypesDefaultMessages.HELLO)
            await answer_with_default_message(
                message_data=hello_message,
                message=message,
                message_type=TypesDefaultMessages.HELLO,
                reply_markup=confirm_gdpr_keyboard
            )
        else:
            raise


@router.callback_query(F.data == 'confirm_gdpr')
async def confirm_gdpr(callback_query: CallbackQuery) -> SendMessage:
    """Обработка согласия gdpr, сохраняет пользователя,
    вызывает главное меню."""
    await create_tg_user(
        {'tg_id': callback_query.from_user.id,
         'nickname': callback_query.from_user.username,
         'gdpr': True}
    )
    await callback_query.message.delete_reply_markup()
    return await callback_query.message.answer(
        MessagesConstants.MAIN, reply_markup=main_keyboard)


@router.callback_query(F.data == 'chat_rules')
async def chat_rules(callback_query: CallbackQuery) -> SendMessage:
    """Показывает правила поведения в чатах,
    одна кнопка вернуться в главное меню."""
    chat_rules = await get_default_message(TypesDefaultMessages.CHAT_RULES)
    await callback_query.message.delete()
    return await answer_with_default_message(
        message_data=chat_rules,
        message=callback_query.message,
        message_type=TypesDefaultMessages.CHAT_RULES,
        reply_markup=back_keyboard
    )


@router.callback_query(F.data == 'knifes')
async def knifes(callback_query: CallbackQuery) -> SendMessage:
    """Список ножей со ссылками, кнопка вернуться в главное меню."""
    knifes = await get_knifes()
    knifes_message = await get_default_message(TypesDefaultMessages.KNIFE)
    knifes_keyboard = get_form_keyboard(back_button)
    await callback_query.message.delete()

    if knifes:
        buttons = [
            InlineKeyboardButton(text=knife.get('name'), callback_data=f"knife {knife.get('name')}")
            for knife in knifes]
        knifes_keyboard = get_form_keyboard(*buttons, back_button)
    return await answer_with_default_message(
        message_data=knifes_message,
        message=callback_query.message,
        message_type=TypesDefaultMessages.KNIFE,
        reply_markup=knifes_keyboard
    )


@router.callback_query(F.data.contains("knife"))
async def knifes(callback_query: CallbackQuery) -> SendMessage:
    """Информация о ноже и кнопка вернуться в главное меню."""
    id = str(callback_query.data.split()[1])
    knife = await get_single_knife(knife_id=id)
    text: str = (f"{knife['pretentious_quote']}\n\nНазвание ножа - {knife['name']}\n"
                 f"Описание - {knife['desc']}\n\nТехнические характеристики:\n"
                 f"Вес в гр - {knife['weight']}\nДлина в мм - {knife['length']}\n"
                 f"Ширина в мм - {knife['width']}\nТолщина в мм - {knife['thickness']}\n\n"
                 f"Особенности:\n{knife['features']}")
    knifes_message: dict = {'text': text, 'image': knife['photo']}
    await callback_query.message.delete()
    knifes_keyboard = get_form_keyboard(knifes_button, back_button)
    return await answer_with_default_message(
        message_data=knifes_message,
        message=callback_query.message,
        message_type=TypesDefaultMessages.KNIFE,
        reply_markup=knifes_keyboard
    )


@router.callback_query(F.data == 'communication_admin')
async def contact_admin(callback_query: CallbackQuery) -> SendMessage:
    """Контакт администратора бота, кнопка вернуться в главное меню."""
    message_admin_contact = await get_default_message(
        TypesDefaultMessages.CONTACT_ADMIN)
    await callback_query.message.delete()
    return await answer_with_default_message(
        message_data=message_admin_contact,
        message=callback_query.message,
        message_type=TypesDefaultMessages.CONTACT_ADMIN,
        reply_markup=back_keyboard
    )


@router.callback_query(F.data == 'back')
async def back_to_main(callback_query: CallbackQuery) -> SendMessage:
    """Вернуться в главное меню."""
    await callback_query.message.delete()
    return await callback_query.message.answer(
        MessagesConstants.MAIN, reply_markup=main_keyboard)


@router.message(Command('about'))
async def about_handler(message: Message) -> SendMessage:
    """Функция бота для команды /about."""
    message_about = await get_default_message(TypesDefaultMessages.ABOUT)
    return await answer_with_default_message(
        message_data=message_about,
        message=message,
        message_type=TypesDefaultMessages.ABOUT,
        reply_markup=None
    )


@router.message(F.text)
async def unknown_command_handler(message: Message) -> SendMessage:
    """Обработка неизвестной команды."""
    message_unknown_command = await get_default_message(
        TypesDefaultMessages.UNKNOWN_COMMAND)
    return await answer_with_default_message(
        message_data=message_unknown_command,
        message=message,
        message_type=TypesDefaultMessages.UNKNOWN_COMMAND,
        reply_markup=None
    )


async def answer_with_default_message(
        message_data: dict,
        message: Message | CallbackQuery,
        message_type: str,
        reply_markup
) -> None:
    """Ответ для базовых сообщений."""
    text = message_data.get('text')
    image_file = await make_image_from_base64(
            message=message_data,
            filename=message_type)
    if not image_file:
        return await message.answer(
            text=text,
            reply_markup=reply_markup)
    else:
        return await message.answer_photo(
            photo=image_file,
            caption=text,
            reply_markup=reply_markup)
