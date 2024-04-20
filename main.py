import app.config as config
import app.messages as msg
import app.keyboards as kb
from app.database import Database
from app.ex_bridge import EXBridge
from app.poller import Poller
import logging

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageToEditNotFound, MessageToDeleteNotFound

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN,
          disable_web_page_preview=True)

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

ex = EXBridge(PATH_EX=config.PATH_EX,
              DIR_EX=config.DIR_EX)

db = Database(PATH_DATABASE=config.PATH_DATABASE,
              ex=ex)

poller = Poller(bot=bot)


class Subscriber(StatesGroup):
    user_id = State()
    duration = State()


class Suspend(StatesGroup):
    user_id = State()

    
class Resume(StatesGroup):
    user_id = State()


class NewUser(StatesGroup):
    user_id = State()
    duration = State()


async def on_startup(_):
    poller.edit_data(await db.get_data())
    asyncio.create_task(poller.check())
    logging.info('Polling started')
    

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    msg_bot_prev = await db.get_data(field='msg_prev', 
                                     user_id=message.chat.id)
                                     
    if msg_bot_prev:
        try:
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=msg_bot_prev)

        except MessageToDeleteNotFound as e:
            logging.error(e)
    status = await db.get_data('status',
                               user_id=message.chat.id)

    msg_bot = await bot.send_message(message.chat.id, 
                                     msg.GREET, 
                                     reply_markup=kb.gen_inline(flag='main', 
                                                                status=status,
                                                                admin=(message.chat.id == config.ID_ADMIN)
                                                                ))

    await db.set_msg_prev_bot(user_id=msg_bot.chat.id,
                              message_id=msg_bot.message_id)


@dp.callback_query_handler(lambda query: query.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, 
                                message_id=msg_bot_prev, 
                                text=msg.HELP)

    status = await db.get_data('status',
                               user_id=callback_query.from_user.id)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline(flag='help', 
                                                                   status=status))
     

@dp.callback_query_handler(lambda query: query.data == 'status')
async def process_query_status(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    start_date = await db.get_data(field='start_date',
                                   user_id=callback_query.from_user.id), 

    end_date = await db.get_data(field='end_date',
                                 user_id=callback_query.from_user.id)

    days_left = await db.get_data(field='days_left',
                                  user_id=callback_query.from_user.id)

    profile_url = await db.get_data(field='profile_url',
                                    user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.STATUS(start_date, end_date, days_left, profile_url), 
                                parse_mode=types.message.ParseMode.MARKDOWN_V2)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline(flag='status'))
 

@dp.callback_query_handler(lambda query: query.data == 'buy')
async def process_query_buy(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.BUY)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.pay)
 

############################################
# ADMIN METHODS 
async def send_payment_info(user_id, user_name): 
    await bot.send_message(chat_id=config.ID_ADMIN,
                           text=msg.PAYMENT(str(user_id), user_name), 
                           reply_markup=kb.pay_confirm,
                           parse_mode=types.message.ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(lambda query: query.data == 'payment_accept')
async def query_payment_accept(callback_query: types.CallbackQuery):
    # user_id = int(callback_query.message.text.split()[0])
    await bot.send_message(callback_query.from_user.id,
                           msg.PAYMENT_SUBSCRIPTION_USER_ID)

    await Subscriber.user_id.set()
    
   
@dp.message_handler(state=Subscriber.user_id)
async def set_subscriber_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['user_id'] = message.text 

        await bot.send_message(chat_id=message.chat.id,
                               text=msg.PAYMENT_SUBSCRIPTION_DURATION)

        await Subscriber.next()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=msg.INPUT_NON_INTEGER)


async def send_confirmation_message(user_id):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=user_id)
    
    profile_url = await db.get_data(field='profile_url',
                                    user_id=user_id) 

    end_date = await db.get_data(field='end_date',
                                 user_id=user_id)
    
    days_left = await db.get_data(field='days_left',
                                  user_id=user_id)

    msg_bot = await bot.send_message(chat_id=user_id,
                                     text=msg.PAYMENT_SUCCESSFUL(end_date, days_left, profile_url),
                                     reply_markup=kb.gen_inline(status='active'),
                                     parse_mode=types.message.ParseMode.MARKDOWN_V2)

    await bot.delete_message(chat_id=user_id,
                             message_id=msg_bot_prev)

    await db.set_msg_prev_bot(user_id=user_id,
                              message_id=msg_bot.message_id)

    poller.edit_data(data=await db.get_data())


@dp.message_handler(state=Subscriber.duration)
async def set_subscription_duration(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            user_id = data['user_id']

        profile_url = await ex.add_user(user_id)
        await db.add_user(user_id=user_id,
                          state='active',
                          duration=int(message.text),
                          profile_url=profile_url)

        await state.finish()
        start_date = await db.get_data(field='start_date',
                                       user_id=user_id)

        end_date = await db.get_data(field='end_date',
                                     user_id=user_id)

        await bot.send_message(chat_id=message.chat.id,
                               text=msg.SUBCRIBER_ADDED(user_id, start_date, end_date),
                               parse_mode=types.message.ParseMode.MARKDOWN_V2)

        await send_confirmation_message(user_id)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=msg.INPUT_NON_INTEGER)
    

@dp.callback_query_handler(lambda query: query.data == 'payment_decline')
async def query_payment_decline(callback_query: types.CallbackQuery):
    user_id = int(callback_query.message.text.split()[0])
    msg_bot = await bot.send_message(chat_id=callback_query.from_user.id,
                                     text=msg.PAYMENT_DECLINE_ADMIN)

    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=user_id)

    await bot.delete_message(chat_id=user_id,
                             message_id=msg_bot_prev)

    msg_bot = await bot.send_message(chat_id=user_id,
                                     text=msg.PAYMENT_DECLINE_USER,
                                     reply_markup=kb.gen_inline())

    await db.set_msg_prev_bot(chat_id=msg_bot.chat.id, 
                              message_id=msg_bot.message_id)
    

@dp.callback_query_handler(lambda query: query.data == 'admin_panel_main')
async def query_admin_panel(callback_query: types.CallbackQuery):
    msg_bot = await bot.send_message(chat_id=callback_query.from_user.id,
                     text=msg.ADMIN_PANEL,
                     reply_markup=kb.gen_inline(flag='admin_main'))

    await db.set_msg_prev_bot(msg_bot.chat.id, msg_bot.message_id)


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_stats')
async def query_admin_panel_stats(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)
    text_status = await db.get_subs_stats()
    
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=text_status)
    
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline(flag='admin_other'))


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_suspend')
async def query_admin_panel_suspend(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)
    
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.ADMIN_AWAIT_USER_ID)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline(flag='admin_other'))

    await Suspend.user_id.set()


@dp.message_handler(state=Suspend.user_id)    
async def admin_panel_suspend_user_set_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        if await db.is_subscription_active(user_id):
            await db.suspend_user(int(user_id))
            await ex.suspend_user(user_id=user_id)
            await bot.send_message(chat_id=message.chat.id,
                             text=msg.ADMIN_USER_SUSPENDED(user_id),
                             parse_mode=types.message.ParseMode.MARKDOWN_V2)
        else:
            await bot.send_message(chat_id=message.chat.id,
                             text=msg.ADMIN_USER_NOT_SUBSCRIBED(user_id),
                             parse_mode=types.message.ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=msg.INPUT_NON_INTEGER)


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_resume')
async def admin_panel_resume(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.ADMIN_AWAIT_USER_ID)
    await Resume.user_id.set()


@dp.message_handler(state=Resume.user_id)
async def admin_panel_resume_user_set_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        if await db.is_subscription_active(user_id):
            start_date = await db.get_start_date(int(user_id))
            end_date = (await db.get_exp_date(int(user_id)))[0]
            await bot.send_message(chat_id=message.chat.id,
                                   text=msg.ADMIN_USER_ALREADY_ACTIVE(user_id, start_date, end_date),
                                   parse_mode=types.message.ParseMode.MARKDOWN_V2,
                                   reply_markup=kb.gen(flag='admin_other'))
        else:
            await db.resume_user(int(user_id))
            await ex.resume_user(user_id)

            start_date = await db.get_start_date(user_id)
            end_date = (await db.get_exp_date(user_id))[0]
            await bot.send_message(chat_id=message.chat.id,
                                   text=msg.ADMIN_USER_RESUMED(user_id, start_date, end_date),
                                   parse_mode=types.message.ParseMode.MARKDOWN_V2,
                                   reply_markup=kb.gen(flag='admin_other'))
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=msg.INPUT_NON_INTEGER)


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_new')
async def admin_panel_new(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.ADMIN_AWAIT_USER_ID)
    await NewUser.user_id.set()
    
    
@dp.message_handler(state=NewUser.user_id)
async def admin_panel_new_set_user_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        if await db.is_subscription_active(user_id):
            start_date = await db.get_start_date(int(user_id))
            end_date = (await db.get_exp_date(int(user_id)))[0]
            await bot.send_message(chat_id=message.chat.id,
                             text=msg.ADMIN_USER_ALREADY_ACTIVE(user_id, start_date, end_date),
                             parse_mode=types.message.ParseMode.MARKDOWN_V2,
                             reply_markup=kb.gen(flag='admin_other'))
        else:
            await db.resume_user(int(user_id))
            await ex.resume_user(user_id)

            
            
            await bot.send_message(chat_id=message.chat.id,
                             text=msg.ADMIN_USER_RESUMED(user_id),
                             parse_mode=types.message.ParseMode.MARKDOWN_V2,
                             reply_markup=kb.gen(flag='admin_other'))
           
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=msg.INPUT_NON_INTEGER)

   
############################################

@dp.callback_query_handler(lambda query: query.data == 'payment')
async def query_payment(callback_query: types.CallbackQuery):
    await send_payment_info(callback_query.from_user.id, callback_query.from_user.username)

    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.PAYMENT_IN_PROCESS)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline())

    await db.add_user(user_id=callback_query.from_user.id,
                      state='in_process')


@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def query_main_menu(callback_query: types.CallbackQuery):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=msg_bot_prev,
                                text=msg.GREET)

    status = await db.get_data(field='status',
                               user_id=callback_query.from_user.id)

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=msg_bot_prev,
                                        reply_markup=kb.gen_inline(flag='main',
                                        status=status,
                                        admin=callback_query.from_user.id == config.ID_ADMIN))


@dp.message_handler()
async def unknown_command(message: types.Message):
    msg_bot_prev = await db.get_data(field='msg_prev',
                                     user_id=message.chat.id)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=msg_bot_prev)

    status = await db.get_data(field='status',
                               user_id=message.chat.id)

    msg_bot = await bot.send_message(chat_id=message.chat.id,
                                     text=msg.UNKNOWN_COMMAND,
                                     reply_markup=kb.gen_inline(status=status))

    await db.set_msg_prev_bot(chat_id=msg_bot.chat.id, 
                              message_id=msg_bot.message_id)

"""
#TODO
переделать клавиатуру
после подтверждения оплаты не вносить новые данные в бд, а обновлять старые
"""


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False, on_startup=on_startup) 