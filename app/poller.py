import asyncio
import datetime as dt


class Poller:
    def __init__(self, countdown: int, bot, data=[]):
        self.data = data
        self.countdown = countdown * 50 * 60 * 24
        self.bot = bot

    def edit_data(self, data: list):
        self.data = data

    async def check(self):
        while True:
            for user in self.data:
                # [(id, user_id, active_subscription, start_date, end_date, profile_url)]
                end_date = [int(x) for x in user[4].split('-')]
                end_date = dt.datetime(day=end_date[0], month=end_date[1], year=end_date[2])
                days_remaining = (end_date - dt.datetime.now()).days 
                if days_remaining <= 7:
                    await self.bot.send_message(chat_id=user[1],
                                                text='Подписка заканчивается через ' + str(days_remaining) + ' дней.')
            await asyncio.sleep(self.countdown)
