from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, ex
from states import Subscriber, Suspend, Resume, NewUser
import keyboards as kb

#TODO
'''
async def send_payment_info(user_id, user_name): 
    msg_bot_prev = await db.get_data(field='msg_bot_prev',
                                     user_id=config.ID_ADMIN)
    await bot.delete_message(chat_id=config.ID_ADMIN,
                             message_id=msg_bot_prev)
    
    msg_bot = await bot.send_message(chat_id=config.ID_ADMIN,
                                     text=msg.PAYMENT(str(user_id), user_name), 
                                     reply_markup=kb.pay_confirm,                                    
                                    parse_mode=types.message.ParseMode.MARKDOWN_V2)

    
    await db.set_msg_bot_prev(user_id=config.ID_ADMIN,
                              message_id=msg_bot.message_id)
'''

#TODO: pass user_id through callback_query
@dp.callback_query_handler(lambda query: query.data and query.data.startswith('payment_accept'))
async def query_payment_accept(callback_query: types.CallbackQuery, state: FSMContext):
    text = 'Введите длительность подписки\:'

    await callback_query.message.edit_text(text)
    
    await state.set_state(Subscriber.user_id)
    user_id = callback_query.data.split(':')[1]
    await state.update_data(user_id=user_id)
    await Subscriber.next()
    
#TODO
'''
async def send_confirmation_message(user_id):
    msg_bot_prev = await db.get_data(field='msg_bot_prev',
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

    await db.set_msg_bot_prev(user_id=user_id,
                              message_id=msg_bot.message_id)

    poller.edit_data(data=await db.get_data())
'''


@dp.message_handler(state=Subscriber.duration)
async def set_subscription_duration(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text.isdigit():
        async with state.proxy() as data:
            user_id = data['user_id']

        profile_url = await ex.add_user(user_id)
        
        await db.activate_subscription(user_id=user_id, 
                                       duration=int(message.text), 
                                       profile_url=profile_url)
        await state.finish()

        start_date = await db.get_data(field='start_date',
                                       user_id=user_id)

        end_date = await db.get_data(field='end_date',
                                     user_id=user_id)

        text = 'Пользователь `{}` добавлен\.\n\nДата оплаты\: {}\nДата истечения подписки\: {}'.format(user_id, '\.'.join(start_date), '\.'.join(end_date))
                             
        await message.answer(text,
                             reply_markup=kb.gen_inline(admin=True))
       
        #TODO
        # await send_confirmation_message(user_id)
    else:
        text = 'Пожалуйста, введите число.'
        await message.answer(text)
    

@dp.callback_query_handler(lambda query: query.data and query.data.startswith('payment_decline'))
async def query_payment_decline(callback_query: types.CallbackQuery):
    text = 'Подписка не была активирована.'
    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(admin=True))

    #TODO
    # await send_decline_message(user_id)
   

@dp.callback_query_handler(lambda query: query.data == 'admin_panel_main')
async def query_admin_panel(callback_query: types.CallbackQuery):
    text = 'Админ панель\.'
    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(flag='admin_main'))


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_stats')
async def query_admin_panel_stats(callback_query: types.CallbackQuery):
    text = await ex.get_stats()
    
    await callback_query.message.edit_text(text)
    
    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(admin=True))


@dp.callback_query_handler(lambda query: query.data == 'admin_panel_suspend')
async def query_admin_panel_suspend(callback_query: types.CallbackQuery):
    #TODO: выводить пользователей с активной подпиской
    text = 'Введите ID пользователя\, подписку которого хотите приостановить\:'
    await callback_query.message.edit_text(text)

    # await callback_query.message.edit_reply_markup(reply_markup=types.ReplyKeyboardRemove())

    await Suspend.user_id.set()


@dp.message_handler(state=Suspend.user_id)    
async def admin_panel_suspend_user_set_id(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        status = await db.get_data(field='status', user_id=user_id)
        if status == 'active':
            await db.set_user_status(user_id=int(user_id),
                                     status='inactive')
            await ex.suspend_user(user_id=user_id)
            text = 'Подписка пользователя с ID `{}` приостановлена\.'.format(user_id)
            await message.answer(text,
                                 reply_markup=kb.gen_inline(admin=True))
            #TODO
            # await send_suspension_message(user_id)
        else:
            text = 'Пользователь с ID `{}` не имеет активной подписки\.'.format(user_id)
            await message.answer(text,
                                 reply_markup=kb.gen_inline(admin=True))
    else:
        text = 'Пожалуйста\, введите число\:'

        await message.answer(text,
                             reply_markup=kb.gen_inline(admin=True))
 

@dp.callback_query_handler(lambda query: query.data == 'admin_panel_resume')
async def query_admin_panel_resume(callback_query: types.CallbackQuery):
    #TODO: выводить пользователей с приостановленной подпиской
    text = 'Введите ID пользователя\, подписку которого хотите возобновить\:'
    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=types.ReplyKeyboardRemove())

    await Resume.user_id.set()


@dp.message_handler(state=Resume.user_id)    
async def admin_panel_resume_user_set_id(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        status = await db.get_data(field='status', user_id=user_id)
        if status == 'inactive':
            await db.set_user_status(user_id=int(user_id),
                                     status='active')
            await ex.resume_user(user_id=user_id)
            text = 'Подписка пользователя с ID `{}` возобновлена\.'.format(user_id)
            await message.answer(text,
                                 reply_markup=kb.gen_inline(admin=True))
            #TODO
            # await send_resumption_message(user_id)
        else:
            text = 'Подписка пользователя с ID `{}` уже активна\.'.format(user_id)
            await message.answer(text,
                                 reply_markup=kb.gen_inline(admin=True))
    else:
        text = 'Пожалуйста\, введите число\:'

        await message.answer(text,
                             reply_markup=kb.gen_inline(admin=True))
 

@dp.callback_query_handler(lambda query: query.data == 'admin_panel_new')
async def admin_panel_new(callback_query: types.CallbackQuery):
    text = 'Введите ID пользователя\, которому хотите выдать подписку\:'
    await callback_query.message.edit_text(text)
    await NewUser.user_id.set()
    
#TODO: 
'''
@dp.message_handler(state=NewUser.user_id)
async def admin_panel_new_set_user_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        user_id = message.text
        await state.finish()
        status = await db.get_data(field='status', user_id=int(user_id))
        if status == 'active':
            start_date = await db.get_data(field='start_date',
                                           user_id=int(user_id))

            end_date = await db.get_data(field='end_date',
                                         user_id=int(user_id))

            text = 'Подписка пользователя с ID `{}` уже активна\.\n\nДата активации\: {}\nДата окончания\: {}'.format(user_id, '\.'.join(start_date), '\.'.join(end_date))
            await message.answer(text,
                                 reply_markup=kb.gen_inline(admin=True))
        else:
            await db.set_user_status(user_id=user_id,
                                     status='active')
            await ex.resume_user(user_id)

            start_date = await db.get_data(field='start_date',
                                           user_id=user_id)

            end_date = await db.get_data(field='end_date',
                                         user_id=user_id)
            
            await bot.edit_message_text(chat_id=config.ID_ADMIN,
                                        message_id=msg_bot_prev,
                                        text=msg.ADMIN_USER_RESUMED(user_id=user_id,
                                                                    start_date=start_date,
                                                                    end_date=end_date),
                                        parse_mode=types.message.ParseMode.MARKDOWN_V2)
            
            await bot.edit_message_reply_markup(chat_id=config.ID_ADMIN,
                                                message_id=msg_bot_prev,
                                                reply_markup=kb.gen_inline(admin=True))
           
    else:
        await bot.edit_message_text(chat_id=config.ID_ADMIN,
                                    message_id=msg_bot_prev,
                                    text=msg.INPUT_NON_INTEGER)
        
        await bot.edit_message_reply_markup(chat_id=config.ID_ADMIN,
                                            message_id=msg_bot_prev,
                                            reply_markup=kb.gen_inline(admin=True))
'''

@dp.callback_query_handler(lambda query: query.data == 'admin_panel_all_users')   
async def admin_panel_all_users(callback_query: types.CallbackQuery):
    data = await db.get_data()
    strings = []
    for user_data in data:
        user_id, status, start_date, end_date = user_data[1:5]
        string = 'ID\: `{}`\nСтатус\: {}\n'.format(user_id, status)
    
        if status == 'active':
            string += 'Дата активации\: {}\nДата окончания\: {}\n'.format(start_date.replace('-', '\-'), end_date.replace('-', '\-'))
    
        strings += [string + '\-' * 15]
    
    text = '\n'.join(strings)

    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(admin=True))

