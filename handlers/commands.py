from aiogram import types,Dispatcher
from config import bot

async def start(message: types.Message):
    await message.answer(f'hello {message.from_user.first_name}')

async def mem(message: types.Message):
    photo = open('media/img.jpg','rb')
    await bot.send_photo(
        photo=photo,
        chat_id=message.from_user.id
    )




def register_commands(dp:Dispatcher):
    dp.register_message_handler(start,commands=['start'])
    dp.register_message_handler(mem,commands=['mem'])