import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))


'''
"message_id": 190,
 
"from": {"id": 269317391, 
         "is_bot": false, 
        "first_name": "Gleb", 
        "username": "jootiee", 
        "language_code": "en", 
        "is_premium": true},
         
"chat": {"id": 269317391, 
         "first_name": "Gleb", 
         "username": "jootiee", 
         "type": "private"}, 

"date": 1713282852, 
"text": "/start", 
"entities": [{"type": "bot_command", "offset": 0, "length": 6}]}


CALLBACK

{
"id": "1156709387736205611", 
"from": {"id": 269317391, 
         "is_bot": false, 
         "first_name": "Gleb", 
         "username": "jootiee", 
         "language_code": "en", 
         "is_premium": true}, 
"message": {"message_id": 406, 
            "from": {"id": 7027862687, 
                     "is_bot": true, 
                     "first_name": "jootieeVPNbot", 
                     "username": "jootieeVPNbot"}, 
            "chat": {"id": 269317391, 
                     "first_name": "Gleb", 
                     "username": "jootiee", 
                     "type": "private"}, 
            "date": 1713286280, 
            "text": "Пользователь 1163175062 совершил оплату. Используйте комманды /decline или /accept для отклонения и подтверждения оплаты соответственно.", 
            "entities": [{"type": "bot_command", 
                          "offset": 62, 
                          "length": 8}, 
                         {"type": "bot_command", 
                         "offset": 75, "length": 7}], 
                         "reply_markup": {"inline_keyboard": [[{"text": "Подтвердить", "callback_data": "payment_accept"}, {"text": "Отказать", "callback_data": "payment_decline"}]]}}, "chat_instance": "-5655774133182036367", "data": "payment_accept"}


'''