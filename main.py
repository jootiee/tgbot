import config
import messages as msg
import keyboards as kb
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# prices
PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=6000)  # в копейках (руб)



# start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, msg.GREET, reply_markup=kb.inline_kb_main_menu)



# help
@dp.callback_query_handler(lambda query: query.data == 'button_help')
async def process_callback_help(callback_query: types.CallbackQuery):
   await bot.answer_callback_query(callback_query.id)
   await bot.send_message(callback_query.from_user.id, msg.HELP)
    
# subscription status 
@dp.callback_query_handler(lambda query: query.data == 'button_subscription_status')
async def process_callback_status(callback_query: types.CallbackQuery):
   await bot.answer_callback_query(callback_query.id)
   await bot.send_message(callback_query.from_user.id, msg.STATUS)
 


# buy
@dp.callback_query_handler(lambda query: query.data == 'button_buy')
async def process_callback_buy(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback_query.from_user.id, "Тестовый платеж!!!")

    await bot.send_invoice(callback_query.from_user.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
 
    
    
# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно.")
    
    
    #TODO: все остальное

@dp.message_handler()
async def failed_payment(message: types.Message):
    await message.reply("Такой команды нет.")


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)