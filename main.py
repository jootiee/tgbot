import app.config as config
import app.messages as msg
import app.keyboards as kb
import app.database as db
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageToEditNotFound, MessageToDeleteNotFound




class NewSubscriber(StatesGroup):
    user_id = State()
    duration = State()


# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN, disable_web_page_preview=True)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db.start()
    print('Bot is running.')


@dp.message_handler(text=['Главное меню', '/start'])
async def start(message: types.Message):
    msg_bot_prev = await db.get_msg_prev_bot(message.chat.id)
    if msg_bot_prev:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_bot_prev)
        except MessageToDeleteNotFound:
            print('aiogram.utils.exceptions.MessageToDeleteNotFound: User has already deleted this message.')
    
    msg_bot = await bot.send_message(message.chat.id, msg.GREET, reply_markup=kb.gen_inline(flag='main', active_subscription=await db.is_subscription_active(message.chat.id)))
    await db.set_msg_prev_bot(msg_bot.chat.id, msg_bot.message_id)


@dp.callback_query_handler(lambda query: query.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, text=msg.HELP)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, reply_markup=kb.gen_inline(flag='help'))
    

@dp.callback_query_handler(lambda query: query.data == 'status')
async def process_query_status(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_msg_prev_bot(callback_query.from_user.id)

    start_date = await db.get_start_date(callback_query.from_user.id), 
    end_date, days_left = await db.get_exp_date(callback_query.from_user.id)
    profile_url = await db.get_profile_url(callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, text=msg.STATUS(start_date, end_date, days_left, profile_url), parse_mode=types.message.ParseMode.MARKDOWN_V2)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, reply_markup=kb.gen_inline())
 

@dp.callback_query_handler(lambda query: query.data == 'buy')
async def process_query_buy(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, text=msg.BUY)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, reply_markup=kb.pay)
 

############################################
# ADMIN METHODS 

async def send_payment_info(user_id, user_name): 
    await bot.send_message(config.ADMIN_ID, msg.PAYMENT.format(str(user_id), user_name, str(user_id)), 
                           reply_markup=kb.pay_confirm, parse_mode=types.message.ParseMode.MARKDOWN_V2)

@dp.callback_query_handler(lambda query: query.data == 'payment_accept')
async def query_payment_accept(callback_query: types.CallbackQuery):
    user_id = int(callback_query.message.text.split()[0])
    await bot.send_message(callback_query.from_user.id, msg.PAYMENT_SUBSCRIPTION_USER_ID)
    await NewSubscriber.user_id.set()
    
   
@dp.message_handler(state=NewSubscriber.user_id)
async def set_subscriber_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['user_id'] = message.text 
        await bot.send_message(message.chat.id, text=msg.PAYMENT_SUBSCRIPTION_DURATION)
        await NewSubscriber.next()
    else:
        await bot.send_message(message.chat.id, text=msg.WRONG_DURATION_INPUT)


async def send_confirmation_message(user_id):
    msg_bot_prev = await db.get_msg_prev_bot(user_id)
    
    profile_url = await db.get_profile_url(user_id)
    
    exp_date, days_left = await db.get_exp_date(user_id)
    
    msg_bot = await bot.send_message(chat_id=user_id, text=msg.PAYMENT_SUCCESSFUL(exp_date, days_left, profile_url), reply_markup=kb.gen_inline(), parse_mode=types.message.ParseMode.MARKDOWN_V2)

    await bot.delete_message(user_id, msg_bot_prev)
    await db.set_msg_prev_bot(user_id, msg_bot.message_id)


@dp.message_handler(state=NewSubscriber.duration)
async def set_subscription_duration(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['duration'] = message.text
            user_id = data['user_id']
        await db.add_user(state)
        await state.finish()
        await bot.send_message(message.chat.id, text=msg.SUBCRIBER_ADDED)
        await send_confirmation_message(user_id)
    else:
        await bot.send_message(message.chat.id, text=msg.WRONG_DURATION_INPUT)
    

@dp.callback_query_handler(lambda query: query.data == 'payment_decline')
async def query_payment_decline(callback_query: types.CallbackQuery):
    user_id = int(callback_query.message.text.split()[0])
    msg_bot = await bot.send_message(callback_query.from_user.id, msg.PAYMENT_DECLINE_ADMIN)

    msg_bot_prev = await db.get_msg_prev_bot(user_id)
    await bot.delete_message(chat_id=user_id, message_id=msg_bot_prev)
    msg_bot = await bot.send_message(user_id, msg.PAYMENT_DECLINE_USER, reply_markup=kb.gen_inline())
    await db.set_msg_prev_bot(msg_bot.chat.id, msg_bot.message_id)
    


############################################

@dp.callback_query_handler(lambda query: query.data == 'payment')
async def query_payment(callback_query: types.CallbackQuery):
    await send_payment_info(callback_query.from_user.id, callback_query.from_user.username)
    msg_bot_prev = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, text=msg.PAYMENT_IN_PROCESS)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, reply_markup=kb.gen_inline())


@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def query_main_menu(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_msg_prev_bot(callback_query.from_user.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, text=msg.GREET)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=msg_bot_prev, reply_markup=kb.gen_inline(flag='main', active_subscription=await db.is_subscription_active(callback_query.from_user.id)))


@dp.message_handler()
async def unknown_command(message: types.Message):
    msg_bot_prev = await db.get_msg_prev_bot(message.chat.id)
    await bot.delete_message(message.chat.id, msg_bot_prev)
    msg_bot = await bot.send_message(message.chat.id, msg.UNKNOWN_COMMAND, reply_markup=kb.gen_inline())
    await db.set_msg_prev_bot(msg_bot.chat.id, msg_bot.message_id)


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