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
                        status TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        profile_url TEXT
                    )
                    ''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS msg_bot_prev
                    (
                        chat_id     INTEGER,
                        message_id  INTEGER
                    )
                    ''')

        self.db.commit()

    async def set_msg_bot_prev(self, user_id: int, message_id: int) -> None:
        if await self.get_data(field='msg_bot_prev', user_id=user_id):
            self.cur.execute('''UPDATE msg_bot_prev SET message_id = (?) WHERE chat_id == (?)
                        ''', (message_id, user_id))
        else:
            self.cur.execute('''
                        INSERT INTO msg_bot_prev (chat_id, message_id) VALUES (?, ?)
                        ''',
                        (user_id, message_id))
        self.db.commit()

    async def add_user(self, user_id: int, state='', duration=0, profile_url='') -> None:
        start_date = (dt.datetime.now()).strftime('%d-%m-%Y')
        end_date = (dt.datetime.now() + dt.timedelta(days=int(duration) + 1)).strftime('%d-%m-%Y')
        self.cur.execute('''
                    INSERT INTO users (user_id, status, start_date, end_date, profile_url) VALUES (?, ?, ?, ?, ?)
                    ''',
                    (user_id, state, start_date, end_date, profile_url))
        self.db.commit()
    
    async def activate_subscription(self, user_id: int, duration: int, profile_url: str):
        start_date = dt.datetime.now().strftime('%d-%m-%Y')
        end_date = (dt.datetime.now() + dt.timedelta(days=duration + 1)).strftime('%d-%m-%Y')
        self.cur.execute('UPDATE users SET status = ?, start_date = ?, end_date = ?, profile_url = ? WHERE user_id == ?',
                         ('active', start_date, end_date, profile_url, user_id))
        self.db.commit()
        
    async def get_data(self, field='', user_id=0):
        result = ''
        if field == 'msg_bot_prev':
            message_id = self.cur.execute('SELECT * FROM msg_bot_prev WHERE chat_id == {}'.format(user_id)).fetchone()
            result = message_id[1] if message_id else 0
        elif field == 'user_exists':
            result = bool(self.cur.execute('SELECT * FROM users WHERE user_id == ?', (user_id,)).fetchone())
        elif field == 'profile_url':
            result = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[5]
        elif field == 'start_date':
            result = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[3].split('-')
        elif field == 'end_date':
            result = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[4].split('-')
        elif field == 'days_left':
            end_date = await self.get_data(field='end_date',
                                           user_id=user_id)
            result = (dt.datetime(day=int(end_date[0]), month=int(end_date[1]), year=int(end_date[2])) - dt.datetime.now()).days
        elif field == 'status':
            if await self.get_data('user_exists', user_id=user_id):
                result = self.cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[2] 
        else:
            result = self.cur.execute('SELECT * from users').fetchall()
        return result

    async def set_user_status(self, user_id: int, status: str):
        self.cur.execute('UPDATE users SET status = ? WHERE user_id == ?', (status, user_id))
        self.db.commit()