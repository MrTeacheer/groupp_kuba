from decouple import config
from aiogram import Bot,Dispatcher,executor,types


token = config('TOKEN')
bot = Bot(token=token)
dp= Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'hello {message.from_user.first_name}')


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)