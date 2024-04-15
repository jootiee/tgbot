import sqlite3 as sq

db = sq.connect('data.db')
cur = db.cursor()

async def db_start():
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        active_subscription INTEGER,
        date_of_payment TEXT,
        date_expiration TEXT
        )
                ''')
    
    db.commit()
    
    
async def is_subscription_active(id):
    pass