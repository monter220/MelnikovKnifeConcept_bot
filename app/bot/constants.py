class MessagesConstants:
    MAIN = 'Выбери один из пунктов'
    NO_USERNAME = ('Пожалуйста, заполни username в настройках профиля '
                   'Телеграм.')
    COMMANDS = {
        '/start': 'Начать работу с чат-ботом.',
        '/about': 'Информация о чат-боте.'
    }
    ERROR = 'Извините, бот сейчас не доступен, пожалуйста попробуйте позже.'
    HELLO = (
        'Привет! \nДобро пожаловать в чат MelnikovKnifeConcept '
        ', где собираются единомышленники. Будем оставаться на '
        'связи и развивать комьюнити метателей. '
        '\n\n\nВ этом чате ты сможешь:\n— находить информацию о ножах '
        'и других проектах Дмитрия Мельникова;\n— получать новости '
        'индустрии;\n— и многое другое!'
    )
    CHAT_RULES = (
        'Правила нашего чата: \n— сохранять пространство для дружелюбного '
        'общения и конструктивной критики;\n— избегать негативных '
        'комментариев или оскорблений;\n— не разглашать конфиденциальную '
        'информацию участников группы.'
    )
    CONTACT_ADMIN = (
        'Если ты захочешь оставить обратную связь, '
        'то можешь написать администратору чата'
    )
    UNKNOWN_COMMAND = (
        'Кажется, я не понял твоё сообщение. '
        'Попробуй ввести другую команду или уточни, '
        'что ты хочешь сделать.'
    )
    KNIFE = 'Описание ножей'
    DESCRIPTION_CHATS = 'Описание чатов'
    ABOUT = 'Я чат-бот. Это мое описание.'


class TypesDefaultMessages:
    HELLO = 'hello'
    CHAT_RULES = 'chat_rules'
    CONTACT_ADMIN = 'contact_admin'
    UNKNOWN_COMMAND = 'unknown_command'
    KNIFE = 'knife'
    ABOUT = 'about'


DEFAULT_MESSAGES_MAP = {
    getattr(TypesDefaultMessages, attr): getattr(MessagesConstants, attr)
    for attr in dir(TypesDefaultMessages) if not attr.startswith('__')
}
