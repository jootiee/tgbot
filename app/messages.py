GREET = "Привет\.\n\nСтоимость подписки\:\nОдин месяц \- _50 рублей_;\nТри месяца \- _135 рублей_;\nПолгода \- _240 рублей_\;\nГод \- _420 рублей_\.\n\nЧтобы купить подписку\, нажми на кнопку снизу ⬇️"

HELP = "По вопросом писать @jootiee\."

BUY = "Для приобретения подписки пишите в личку @jootiee\.\nПосле оплаты\, нажмите на кнопку *Я оплатил* снизу"

INPUT_NON_INTEGER = '''Пожалуйста, введите число.'''

UNKNOWN_COMMAND = '''Такой команды нет'''

PAYMENT_IN_PROCESS = """Пожалуйста, подождите, пока я проверяю вашу оплату."""

ADMIN_PANEL = '''Админ панель.'''

PAYMENT_DECLINE_ADMIN = '''Подписка не была активирована.'''

PAYMENT_DECLINE_USER = '''Оплата не была произведена. Подписка не была активирована.'''

ADMIN_AWAIT_USER_ID = '''Введите ID пользователя:'''

ADMIN_AWAIT_SUBSCRIPTION_DURATION = '''Введите длительность подписки:'''


def PAYMENT(user_id: str, user_name: str) -> str:
    string = """`{}` совершил оплату\.\n\n\nЮзернейм\: \@{}\nСсылка: tg\:\/\/user\?id\={}"""
    return string.format(user_id, user_name, user_id)


def get_days_left(days_left: int) -> str:
    string_days_left = ''

    if days_left % 10 == 1:
        string_days_left += str(days_left) + '  день'
    elif 5 <= days_left <= 20:
        string_days_left += str(days_left) + ' дней'
    elif 2 <= days_left % 10 <= 4:
        string_days_left += str(days_left) + ' дня'
    else:
        string_days_left += str(days_left) + ' дней'
    return string_days_left
 

def PAYMENT_SUCCESSFUL(end_date, days_left, profile_url):
    string = '''Подписка оплачена успешно\!\nДата истечения подписки\: {} \({}\)\.\n\nГайд по установке\: \([ссылка](https://jootiee.notion.site/VPN-Setup-0d66f241451747bfaf26e701c5a1c0fc?pvs=4)\)\n\nПрофиль \(нажмите на неё\, чтобы скопировать\)\:\n`{}`'''
    return string.format('\.'.join(end_date), get_days_left(days_left), profile_url)
 

def STATUS(start_date, end_date, days_left, profile_url):
    string = """Подписка активна\.\n\nДата начала подписки\: {}\nДата истечения подписки\: {} \({}\)\n\nГайд по установке\: \([ссылка](https://jootiee.notion.site/VPN-Setup-0d66f241451747bfaf26e701c5a1c0fc?pvs=4)\)\n\nСсылка на профиль \(нажмите на неё\, чтобы скопировать\)\:\n`{}`"""
    return string.format('\.'.join(start_date[0]), '\.'.join(end_date), get_days_left(days_left), profile_url)


def SUBCRIBER_ADDED(user_id: int, start_date: list, end_date: list) -> str:
    string = 'Пользователь `{}` добавлен\.\n\nДата оплаты\: {}\nДата истечения подписки\: {}'
    return string.format(user_id, '\.'.join(start_date), '\.'.join(end_date))


def ADMIN_USER_SUSPENDED(user_id: str) -> str:
    string = '''Подписка пользователя с ID `{}` приостановлена\.'''
    return string.format(user_id)


def ADMIN_USER_NOT_SUBSCRIBED(user_id: str) -> str:
    string = '''Пользователь с ID `{}` не имеет активной подписки\.'''
    return string.format(user_id)


def ADMIN_USER_ALREADY_ACTIVE(user_id: str, start_date: list, end_date: list) -> str:
    string = '''Подписка пользователя с ID `{}` уже активна\.\n\nДата активации\: {}\nДата окончания\: {}'''
    return string.format(user_id, '\.'.join(start_date), '\.'.join(end_date))


def ADMIN_USER_RESUMED(user_id: str, start_date: list, end_date: list) -> str:
    string = '''Подписка пользователя с ID `{}` возобновлена\.\n\nДата активации\n: {}\nДата окончания\: {}'''
    return string.format(user_id, '\.'.join(start_date), '\.'.join(end_date))


def ADMIN_USER_DATA(user_data: list) -> str:
    user_id, status, start_date, end_date = user_data[1:5]
    string = 'ID\: `{}`\nСтатус\: {}\n'.format(user_id, status)
    
    if status == 'active':
        string += 'Дата активации\: {}\nДата окончания\: {}\n'.format(start_date.replace('-', '\-'), end_date.replace('-', '\-'))
    
    string += '\-' * 15
    
    return string
