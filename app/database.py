import sqlite3 as sq
import datetime as dt


class Database:
    def __init__(self, PATH_DATABASE: str, ex):
        self.db = sq.connect(PATH_DATABASE)
        self.cur = self.db.cursor()
        self.ex = ex

        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        active_subscription INTEGER,
                        start_date TEXT,
                        end_date TEXT,
                        profile_url TEXT
                    )
                    ''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS msg_prev_bot
                    (
                        chat_id     INTEGER,
                        message_id  INTEGER
                    )
                    ''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS msg_prev_user
                    (
                        chat_id     INTEGER,
                        message_id  INTEGER
                    )
                    ''')
        
        
        self.db.commit()
        
        return None
 
    async def get_msg_prev_bot(self, chat_id: int) -> int:
        message_id = self.cur.execute('''
                                SELECT * FROM msg_prev_bot WHERE chat_id == {}
                                '''.format(chat_id)).fetchone()
        
        return message_id[1] if message_id else 0


    async def set_msg_prev_bot(self, chat_id: int, message_id: int) -> None:
        if await self.get_msg_prev_bot(chat_id):
            self.cur.execute('''UPDATE msg_prev_bot SET message_id = (?) WHERE chat_id == (?)
                        ''', (message_id, chat_id))
        else:
            self.cur.execute('''
                        INSERT INTO msg_prev_bot (chat_id, message_id) VALUES (?, ?)
                        ''',
                        (chat_id, message_id))
        self.db.commit()


    async def add_user(self, state, profile_url: str) -> None:
        async with state.proxy() as data:
            user_id = data['user_id']
            duration = data['duration']
        start_date = (dt.datetime.now()).strftime('%d-%m-%Y')
        end_date = (dt.datetime.now() + dt.timedelta(days=int(duration) + 1)).strftime('%d-%m-%Y')
        self.cur.execute('''
                    INSERT INTO users (user_id, active_subscription, start_date, end_date, profile_url) VALUES (?, ?, ?, ?, ?)
                    ''',
                    (user_id, 1, start_date, end_date, profile_url))
        self.db.commit()
        

    async def is_user_exist(self, user_id: int) -> bool:
        return bool(self.cur.execute('SELECT * FROM users WHERE user_id == ?', (user_id,)).fetchone())


    async def get_profile_url(self, user_id) -> str:
        profile_url = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[5]
        return profile_url

    async def get_start_date(self, user_id) -> list:
        start_date = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[3].split('-')
        return start_date


    async def get_exp_date(self, user_id: int) -> list:
        exp_date = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[4].split('-')
        days_left = (dt.datetime(day=int(exp_date[0]), month=int(exp_date[1]), year=int(exp_date[2])) - dt.datetime.now()).days
        return (exp_date, days_left)


    async def is_subscription_active(self, user_id: int) -> None:
        return self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[2] == 1 if await self.is_user_exist(user_id) else False


    async def suspend_user(self, user_id: int) -> None:
        self.cur.execute('UPDATE users SET active_subscription = 0 WHERE user_id == ?', (user_id,))
        self.db.commit()
        

    async def resume_user(self, user_id: int) -> None:
        self.cur.execute('UPDATE users SET active_subscription = 1 WHERE user_id == ?', (user_id,))
        self.db.commit()

        
    async def get_data(self) -> list:
        return self.cur.execute('SELECT * from users').fetchall()