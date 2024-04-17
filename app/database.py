import sqlite3 as sq

db = sq.connect('data.db')
cur = db.cursor()

async def start():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        active_subscription INTEGER,
        date_of_payment TEXT,
        date_expiration TEXT
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
                             '''.format(chat_id)).fetchone()[1]
    return message_id


async def set_msg_prev_bot(chat_id, message_id):
    if await get_msg_prev_bot(chat_id):
        cur.execute('''UPDATE msg_prev_bot SET message_id = (?) WHERE chat_id == (?)
                    ''', (message_id, chat_id))
    else:
        cur.execute('''
                    INSERT INTO msg_prev_bot (chat_id, message_id) VALUES (?, ?)
                    ''',
                    (chat_id, message_id))
    db.commit()

    
async def is_subscription_active(id):
    pass