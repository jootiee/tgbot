GREET = """Привет! Чтобы приобрести подписку на VPN..."""

HELP = """Помощь."""

BUY = """Приобрести подписку."""

def SUBCRIBER_ADDED(user_id, start_date, end_date):
    string = 'Пользователь `{}` добавлен\.\n\nДата оплаты\: {}\nДата истечения подписки\: {}'
    return string.format(user_id, '\.'.join(start_date), '\.'.join(end_date))

INPUT_NON_INTEGER = '''Пожалуйста, введите число.'''

UNKNOWN_COMMAND = '''Такой команды нет'''

PAYMENT = """`{}` совершил оплату\.\n\n\nЮзернейм\: \@{}\nСсылка: tg\:\/\/user\?id\={}"""

PAYMENT_IN_PROCESS = """Пожалуйста, подождите, пока я проверяю вашу оплату."""

PAYMENT_SUBSCRIPTION_USER_ID = '''Введите ID пользователя:'''

PAYMENT_SUBSCRIPTION_DURATION = '''Введите длительность подписки:'''

def get_days_left(days_left):
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


ADMIN_PANEL = '''Админ панель.'''

PAYMENT_DECLINE_ADMIN = '''Подписка не была активирована.'''

PAYMENT_DECLINE_USER = '''Оплата не была произведена. Подписка не была активирована.'''

ADMIN_SUSPEND_USER_ID = '''Введите ID пользователя:'''

ADMIN_USER_SUSPENDED = '''Подписка пользователя с ID `{}` приостановлена\.'''

ADMIN_USER_NOT_SUBSCRIBED = '''Пользователь с ID `{}` не имеет активной подписки\.'''