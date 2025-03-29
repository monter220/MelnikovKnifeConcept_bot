from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_form_keyboard(*buttons):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    return builder.as_markup()


chat_rules_button = InlineKeyboardButton(
    text='Правила чатов',
    callback_data='chat_rules'
)
knifes_button = InlineKeyboardButton(
    text='Ножи',
    callback_data='knifes'
)
communication_admin_button = InlineKeyboardButton(
    text='Связь с администратором',
    callback_data='communication_admin'
)
confirm_gdpr_button = InlineKeyboardButton(
    text='Разрешить',
    callback_data='confirm_gdpr'
)
back_button = InlineKeyboardButton(
    text='Назад',
    callback_data='back'
)


main_keyboard = get_form_keyboard(
    chat_rules_button,
    knifes_button,
    communication_admin_button
)
confirm_gdpr_keyboard = get_form_keyboard(
    confirm_gdpr_button
)
back_keyboard = get_form_keyboard(
    back_button
)
