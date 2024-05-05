import asyncio
import datetime as dt


class Poller:
    def __init__(self, bot, data=[]):
        self.data = data
        self.bot = bot

    def edit_data(self, data: list):
        self.data = data

    async def check(self):
        while True:
            closest_date = dt.datetime(day=1, month=1, year=2030)
            for user in self.data:
                # [(id, user_id, active_subscription, start_date, end_date, profile_url)]
                end_date = [int(x) for x in user[4].split('-')]
                end_date = dt.datetime(day=end_date[0], month=end_date[1], year=end_date[2])
                days_remaining = (end_date - dt.datetime.now()).days 
                if days_remaining <= 7:
                    await self.bot.send_message(chat_id=user[1],
                                                text='Подписка заканчивается через ' + str(days_remaining) + ' дней.')
                closest_date = min(closest_date, end_date)
            countdown = (closest_date - dt.datetime.now()).total_seconds()
            await asyncio.sleep(countdown)
