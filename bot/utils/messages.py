import datetime
from dateutil.relativedelta import relativedelta

GUIDE_URL = "https\://google\.com/"

months = {
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

main_unsubscribed = (
    '''Привет\!
    Просто сервис\.'''
)

buy_info = """Для покупки введите команду \/buy и через пробел целым числом укажите количество дней\.
Один день подписки \- одна звезда\."""

help = "По вопросом писать \@jootiee\."

unknown_query = "Неизвестный запрос\. Проверьте корректность ввода и попробуйте снова\."

def pretty_date(
    date: str
) -> str:
    "2025-03-09T00:16:27Z"
    
    date_pretty, time_pretty = date[:16].split("T")
    date_pretty = date_pretty.split("-")[::-1]
    time_pretty = time_pretty.replace(":", "\:")
    result = f"{str(int(date_pretty[0]))} {months[int(date_pretty[1])]} {date_pretty[2]}\, {time_pretty}"
    return result

def pretty_duration(
    expiration_date: str
) -> str: 
    start_datetime =    datetime.datetime.now()
    expiration_datetime =      datetime.datetime.strptime(expiration_date[:10], "%Y-%m-%d")
    result = ""

    diff = relativedelta(expiration_datetime, start_datetime)
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
    expiration_date:       str,
    profile_url:    str
):    
    text = """Подписка активна\.
Срок\: до {} \({}\)\.
    
Ссылка на гайд\: {}
    
Ссылка на профиль\: {}""".format(
    pretty_date(expiration_date),
    pretty_duration(expiration_date),
    GUIDE_URL,
    '`' + profile_url + '`'
    )
    return text

    

