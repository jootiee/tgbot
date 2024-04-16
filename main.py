import app.config as config
import app.messages as msg
import app.keyboards as kb
import logging

from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN, disable_web_page_preview=True)
dp = Dispatcher(bot)

# Consists of previous messages in chats: 'chat_id': 'message_id'
msg_prev_bot = dict()
msg_prev_user = dict()


async def delete_prev_msg(msg_bot, msg_user):
    global msg_prev_bot, msg_prev_user
    if msg_bot['chat']['id'] in msg_prev_bot.keys():
        await bot.delete_message(chat_id=msg_bot['chat']['id'], message_id=msg_prev_bot[msg_bot['chat']['id']])
    if msg_user:
        if msg_user['chat']['id'] in msg_prev_user.keys():
            await bot.delete_message(chat_id=msg_user['chat']['id'], message_id=msg_prev_user[msg_user['chat']['id']])
        msg_prev_user[msg_user['chat']['id']] = msg_user['message_id']

    msg_prev_bot[msg_bot['chat']['id']] = msg_bot['message_id']
    
@dp.message_handler(text=['Главное меню', '/start'])
async def start(message: types.Message):
    msg_bot = await bot.send_message(message.chat.id, msg.GREET, reply_markup=kb.gen(flag='main'))
    await delete_prev_msg(msg_bot, message)

@dp.message_handler(text=['Помощь'])
async def help(message: types.Message):
    msg_bot = await bot.send_message(message.chat.id, msg.HELP, reply_markup=kb.gen(flag='help'))
    await delete_prev_msg(msg_bot, message)
    
@dp.message_handler(text=['Статус подписки'])
async def subscription_status(message: types.Message):
   msg_bot = await bot.send_message(message.chat.id, msg.STATUS, reply_markup=kb.gen())
   await delete_prev_msg(msg_bot, message)
 
@dp.message_handler(text=['Приобрести подписку'])
async def buy(message: types.Message):
    msg_bot = await bot.send_message(message.chat.id, msg.BUY, reply_markup=kb.pay)
    await delete_prev_msg(msg_bot, message)


############################################
# ADMIN METHODS 

async def send_payment_info(user_id, user_name): 
    await bot.send_message(config.ADMIN_ID, msg.PAYMENT.format(str(user_id), user_name, str(user_id)), 
                           reply_markup=kb.pay_confirm)

@dp.callback_query_handler(lambda query: query.data == 'payment_accept')
async def query_payment_accept(callback_query: types.CallbackQuery):
    user_id = int(callback_query['message']['text'].split()[0])
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_SUBSCRIPTION_DURATION)
    await delete_prev_msg(msg_bot, 0)
    # TODO: доделать ввод длительности подписки (посмотреть про FSM автоматы), выдачу ссылки на профиль

    profile_url = ''

    msg_bot = await bot.send_message(user_id, msg.PAYMENT_SUCCESSFUL.format(profile_url), 
                                     parse_mode=types.message.ParseMode.MARKDOWN_V2)
    await delete_prev_msg(msg_bot, 0)

@dp.callback_query_handler(lambda query: query.data == 'payment_decline')
async def query_payment_decline(callback_query: types.CallbackQuery):
    user_id = int(callback_query['message']['text'].split()[0])
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_DECLINE_ADMIN)
    await delete_prev_msg(msg_bot, 0)
    msg_bot = await bot.send_message(user_id, msg.PAYMENT_DECLINE_USER)
    await delete_prev_msg(msg_bot, 0)


############################################

@dp.callback_query_handler(lambda query: query.data == 'payment')
async def query_payment(callback_query: types.CallbackQuery):
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_IN_PROCESS, reply_markup=kb.gen())
    await delete_prev_msg(msg_bot, 0)
    await send_payment_info(callback_query.from_user.id, callback_query.from_user.username)

@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def query_main_menu(callback_query: types.CallbackQuery):
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.GREET, reply_markup=kb.gen(flag='main'))
    await delete_prev_msg(msg_bot, 0)
    

@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.reply("Такой команды нет.")

'''
TODO:
реализовать взаимодействие с бд:
занесение пользователя в бд ПРИ ПОКУПКЕ - даты оплаты, даты истечения платежа
хранение ссылок на профили пользователей

реализовать выдачу ссылки пользователю
реализовать деактивацию ссылки пользователя

реализовать напоминание об истечении подписки
'''

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)