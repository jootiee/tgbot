import datetime
from aiogram.utils import markdown
from dateutil.relativedelta import relativedelta


STARTUP = markdown.text(
    "Bot is running:",
    datetime.datetime.strftime(
        datetime.datetime.now(), "%Y\\-%m\\-%d %H\\:%M\\:%S"))

SHUTDOWN = markdown.text(
    "Bot is stopped:",
    datetime.datetime.strftime(
        datetime.datetime.now(), "%Y\\-%m\\-%d %H\\:%M\\:%S"))


GUIDE_URL = "https\\://google\\.com/"

MONTHS = {
    1:  "января",
    2:  "февраля",
    3:  "марта",
    4:  "апреля",
    5:  "мая",
    6:  "июня",
    7:  "июля",
    8:  "августа",
    9:  "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}

MAIN_INACTIVE = markdown.text(
    "Привет\\!",
    "Просто сервис\\."
)

PAYMENT_INFO = markdown.text(
    "Для покупки введите команду \\/buy и через пробел целым числом укажите количество дней\\.",
    "Один день подписки \\- одна звезда\\.",
    sep="\n"
)

PAYMENT_UNAVAILABLE_ALREADY_SUBSCRIBED = "Вы не можете купить подписку\\, так как она у вас уже активна\\."

PAYMENT_WRONG_INPUT = "Через пробел необходимо указать целое число \\- желаемую длительность подписки в днях\\. Попробуйте еще раз\\."

PAYMENT_PROCESSED_SUCCESS = "Оплата произведена успешно\\."

PAYMENT_PROCESSED_FAIL = "Возникла ошибка при попытке оплаты\\. Если вы считаете\\, что это ошибка\\, свяжитесь с поддержкой\\."

HELP = "По вопросом писать \\@jootiee\\."

UNKNOWN_QUERY = "Неизвестный запрос\\. Проверьте корректность ввода и попробуйте снова\\."

NOT_FOUND = "Ничего не найдено\\. Если вы считаете\\, что это ошибка\\, свяжитесь с поддержкой\\."

ADMIN_GET_CLIENTS_FAILURE = "Не удалось получить список клиентов\\."


ADMIN_CLIENT_INFO = markdown.text(
    "Telegram ID: {}",
    "Telegram username: @{}",
    "Дата истечения: {}",
    "AWG ID: {}",
    sep="\n"
)

ADMIN_ADD_CLIENT_WRONG_INPUT = markdown.text(
    "Некорректный ввод\\.",
    "Через пробел необходимо указать id клиента \\(целое число\\)\\, никнейм в Telegram и длительность подписки в днях \\(целое число\\)\\."
    "Пример: /client 1234567890 durov 52\\.",
    sep="\n"
)

ADMIN_ADD_CLIENT_SUCCESS = markdown.text(
    "Клиент успешно добавлен\\.",
    "ID клиента в AWG\\: {}",
    sep="\n"
)

ADMIN_ADD_CLIENT_FAILURE = markdown.text(
    "Не удалось добавить клиента {} - {}\\.",
    "Проверьте корректность ввода и попробуйте снова\\.",
    sep="\n"
)

ADMIN_REFUND_PAYMENT_WRONG_INPUT = markdown.text(
    "Некорректный ввод\\.",
    "Через пробел необходимо указать id транзакции \\(строка\\)."
    "Пример: /refund stxHiqdhhLlzcmiFPJJ7iVkD9f7Z\\-g1kxeJLJgb3rqS\\-26b5Wh5\\_jU\\-pTtkqsba7lLC\\_R8T0fQJX2AYCxXyvtBckZM5xgOMxuP\\-aLHThEG3TnI\\.",
    sep="\n"
)

ADMIN_REFUND_PAYMENT_SUCCESS = markdown.text(
    "Возврат произведен успешно\\.",
    "ID транзакции \\: {}",
    sep="\n"
)


def pretty_date(
    date: str
) -> str:
    date_pretty, time_pretty = date[:16].split("T")
    date_pretty = date_pretty.split("-")[::-1]
    time_pretty = time_pretty.replace(":", "\\:")
    result = f"{str(int(date_pretty[0]))} {MONTHS[int(date_pretty[1])]} {date_pretty[2]}\\, {time_pretty}"
    return result


def pretty_duration(
    expires_at: str
) -> str:
    start_datetime = datetime.datetime.now(
        # tz=datetime.timezone(
        #     datetime.timedelta(hours=3)
        # )
    )
    expires_at_datetime = datetime.datetime.strptime(
        expires_at[:10], "%Y-%m-%d"
    )
    result = ""

    diff = relativedelta(expires_at_datetime, start_datetime)
    years, months, days = diff.years, diff.months % 12, diff.days
    if years:
        if years == 1:
            years_suffix = " год "
        elif 2 <= years <= 4:
            years_suffix = " года "
        else:
            years_suffix = " лет "
        result += str(years) + years_suffix
    if months:
        if months == 1:
            months_suffix = " месяц "
        elif 2 <= months <= 4:
            months_suffix = " месяца "
        else:
            months_suffix = " месяцев "
        result += str(months) + months_suffix
    if days:
        if days in (1, 21, 31):
            days_suffix = " день"
        elif (2 <= days <= 4) or (22 <= days <= 24):
            days_suffix = " дня"
        elif (5 <= days <= 20) or (25 <= days <= 30):
            days_suffix = " дней"
        result += str(days) + days_suffix
    return result.rstrip()


def gen_main_subscribed(
    expires_at:       str,
) -> str:
    text = markdown.text(
        "Подписка активна\\.",
        f"Срок\\: до {pretty_date(expires_at)} \\({pretty_duration(expires_at)}\\)\\.",
        f"Ссылка на гайд\\: {GUIDE_URL}",
        sep="\n"
    )
    return text
