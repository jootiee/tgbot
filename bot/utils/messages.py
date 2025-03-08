import datetime
from dateutil.relativedelta import relativedelta

main_unsubscribed = (
    '''Привет\!\n
    asdads'''
)

help = "По вопросом писать \@jootiee\."

purchase = "Для приобретения подписки пишите в личку @jootiee\.\nПосле оплаты\, нажмите на кнопку *Я оплатил* снизу"

unknown_query = "Неизвестный запрос\. Проверьте корректность ввода и попробуйте снова\."

main_subscribed = """Подписка активна\.\n{} {} \({}\)\n\nСсылка на гайд\: {}\n\nСсылка на профиль\: {}"""

# TODO: вынести в utils
def format_duration(start, exp: datetime.datetime) -> str: 
    result = ""
    diff = relativedelta(exp, start)
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
    return result