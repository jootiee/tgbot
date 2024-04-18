import sqlite3 as sq
import datetime as dt
import app.ex_bridge as ex
db = sq.connect('data.db')
cur = db.cursor()


async def start():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        active_subscription INTEGER,
        start_date TEXT,
        end_date TEXT,
        profile_url TEXT
            )
                ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS msg_prev_bot
                (
                    chat_id     INTEGER,
                    message_id  INTEGER
                )
                ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS msg_prev_user
                (
                    chat_id     INTEGER,
                    message_id  INTEGER
                )
                ''')
    
    
    db.commit()
 
     
async def get_msg_prev_user(chat_id):
    message_id = cur.execute('''SELECT * FROM msg_prev_user WHERE chat_id == {key}
                             '''.format(key=chat_id)).fetchone()
    return int(message_id)


async def set_msg_prev_user(chat_id, message_id):
    cur.execute('''
                INSERT INTO msg_prev_user (chat_id, message_id) VALUES (?, ?)
                ''',
                (chat_id, message_id))
    db.commit()


async def get_msg_prev_bot(chat_id):
    message_id = cur.execute('''
                             SELECT * FROM msg_prev_bot WHERE chat_id == {}
                             '''.format(chat_id)).fetchone()
    
    return message_id[1] if message_id else 0


async def set_msg_prev_bot(chat_id, message_id, text=''):
    if await get_msg_prev_bot(chat_id):
        cur.execute('''UPDATE msg_prev_bot SET message_id = (?) WHERE chat_id == (?)
                    ''', (message_id, chat_id))
    else:
        cur.execute('''
                    INSERT INTO msg_prev_bot (chat_id, message_id) VALUES (?, ?)
                    ''',
                    (chat_id, message_id))
    db.commit()


async def add_user(state):
    async with state.proxy() as data:
        user_id = data['user_id']
        duration = data['duration']
    start_date = (dt.datetime.now()).strftime('%d-%m-%Y')
    end_date = (dt.datetime.now() + dt.timedelta(days=int(duration) + 1)).strftime('%d-%m-%Y')
    profile_url = await ex.add_user(user_id)
    cur.execute('''
                INSERT INTO users (user_id, active_subscription, start_date, end_date, profile_url) VALUES (?, ?, ?, ?, ?)
                ''',
                (user_id, 1, start_date, end_date, profile_url))
    db.commit()
    

async def is_user_exist(user_id):
    return bool(cur.execute('SELECT * FROM users WHERE user_id == ?', (user_id,)).fetchone())


async def get_profile_url(user_id) -> str:
    profile_url = cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[5]
    return profile_url

async def get_start_date(user_id):
    start_date = cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[3].split('-')
    return start_date


async def get_exp_date(user_id):
    exp_date = cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[4].split('-')
    days_left = (dt.datetime(day=int(exp_date[0]), month=int(exp_date[1]), year=int(exp_date[2])) - dt.datetime.now()).days
    return (exp_date, days_left)


async def get_subs_stats():
    return await ex.get_stats()
    

async def is_subscription_active(user_id):
    return cur.execute('SELECT * from users WHERE user_id == ?', (user_id,)).fetchone()[2] == 1 if await is_user_exist(user_id) else False


async def suspend_user(user_id):
    cur.execute('UPDATE users SET active_subscription = 0 WHERE user_id == ?', (user_id,))
    db.commit()