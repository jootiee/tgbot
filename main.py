import app.config as config
import app.messages as msg
import app.keyboards as kb
import app.database as db
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageToEditNotFound, MessageToDeleteNotFound


# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN, disable_web_page_preview=True)
dp = Dispatcher(bot)

async def on_startup(_):
    await db.start()
    print('Bot is running.')


@dp.message_handler(text=['Главное меню', '/start'])
async def start(message: types.Message):
    prev_msg = await db.get_msg_prev_bot(message.chat.id)
    if prev_msg:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=prev_msg)
        except MessageToDeleteNotFound:
            print('aiogram.utils.exceptions.MessageToDeleteNotFound: User has already deleted this message.')
    
    msg_bot = await bot.send_message(message.chat.id, msg.GREET, reply_markup=kb.gen_inline(flag='main'))
    await db.set_msg_prev_bot(msg_bot['chat']['id'], msg_bot['message_id'])


@dp.callback_query_handler(lambda query: query.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    prev_msg = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=prev_msg, text=msg.HELP)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=prev_msg, reply_markup=kb.gen_inline(flag='help'))
    

@dp.callback_query_handler(lambda query: query.data == 'status')
async def process_query_status(callback_query: types.CallbackQuery):
    prev_msg = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=prev_msg, text=msg.STATUS)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=prev_msg, reply_markup=kb.gen_inline())
 

@dp.callback_query_handler(lambda query: query.data == 'buy')
async def process_query_buy(callback_query: types.CallbackQuery):
    prev_msg = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=prev_msg, text=msg.BUY)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=prev_msg, reply_markup=kb.pay)
 

############################################
# ADMIN METHODS 

async def send_payment_info(user_id, user_name): 
    await bot.send_message(config.ADMIN_ID, msg.PAYMENT.format(str(user_id), user_name, str(user_id)), 
                           reply_markup=kb.pay_confirm)

@dp.callback_query_handler(lambda query: query.data == 'payment_accept')
async def query_payment_accept(callback_query: types.CallbackQuery):
    user_id = int(callback_query['message']['text'].split()[0])
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_SUBSCRIPTION_DURATION)
    # TODO: доделать ввод длительности подписки (посмотреть про FSM автоматы), выдачу ссылки на профиль

    profile_url = ''

    msg_bot = await bot.send_message(user_id, msg.PAYMENT_SUCCESSFUL.format(profile_url), 
                                     parse_mode=types.message.ParseMode.MARKDOWN_V2)
    # await delete_prev_msg(msg_bot, 0)

@dp.callback_query_handler(lambda query: query.data == 'payment_decline')
async def query_payment_decline(callback_query: types.CallbackQuery):
    user_id = int(callback_query['message']['text'].split()[0])
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_DECLINE_ADMIN)
    # await delete_prev_msg(msg_bot, 0)
    msg_bot = await bot.send_message(user_id, msg.PAYMENT_DECLINE_USER)
    # await delete_prev_msg(msg_bot, 0)


############################################

@dp.callback_query_handler(lambda query: query.data == 'payment')
async def query_payment(callback_query: types.CallbackQuery):
    await send_payment_info(callback_query.from_user.id, callback_query.from_user.username)
    prev_msg = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=prev_msg, text=msg.PAYMENT_IN_PROCESS)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=prev_msg, reply_markup=kb.gen_inline())
 
@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def query_main_menu(callback_query: types.CallbackQuery):
    prev_msg = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=prev_msg, text=msg.GREET)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=prev_msg, reply_markup=kb.gen_inline(flag='main'))

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
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)