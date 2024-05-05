from aiogram import types

from loader import dp, db
import keyboards as kb


@dp.callback_query_handler(lambda query: query.data == 'status')
async def process_query_status(callback_query: types.CallbackQuery):
    start_date = await db.get_data(field='start_date',
                                   user_id=callback_query.from_user.id), 

    end_date = await db.get_data(field='end_date',
                                 user_id=callback_query.from_user.id)

    days_left = await db.get_data(field='days_left',
                                  user_id=callback_query.from_user.id)

    profile_url = await db.get_data(field='profile_url',
                                    user_id=callback_query.from_user.id)
    string_days_left = ''

    if days_left % 10 == 1:
        string_days_left += str(days_left) + '  день'
    elif 5 <= days_left <= 20:
        string_days_left += str(days_left) + ' дней'
    elif 2 <= days_left % 10 <= 4:
        string_days_left += str(days_left) + ' дня'
    else:
        string_days_left += str(days_left) + ' дней'
 
    text = "Подписка активна\.\n\nДата начала подписки\: {}\nДата истечения подписки\: {} \({}\)\n\nГайд по установке\: \([ссылка](https://jootiee.notion.site/VPN-Setup-0d66f241451747bfaf26e701c5a1c0fc?pvs=4)\)\n\nСсылка на профиль \(нажмите на неё\, чтобы скопировать\)\:\n`{}`".format('\.'.join(start_date[0]), '\.'.join(end_date), string_days_left, profile_url)




    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(flag='status'))
 