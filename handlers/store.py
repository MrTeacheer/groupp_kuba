from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Store(StatesGroup):
    name =State()
    size = State()
    category = State()
    price = State()
    photo = State()


async def start_fsm(message:types.Message):
    await message.answer('name of prod?')
    await Store.name.set()


async def process_name(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    kb= types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton(text = 'S')
    b2 = types.KeyboardButton(text = 'M')
    b3 = types.KeyboardButton(text = 'L')
    kb.add(b1,b2,b3)
    await message.answer('what is the size',reply_markup=kb)
    await Store.next()

async def process_size(message:types.Message,state:FSMContext):
    kb = types.ReplyKeyboardRemove()
    if message.text in ('L','M','S'):
        async with state.proxy() as data:
            data['size'] = message.text
        await message.answer('category of prod?',reply_markup=kb)
        await Store.next()
    else:
        await message.answer('press only buttons!!!')


async def process_cat(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
            data['cat'] = message.text
    await message.answer('price of prod?')
    await Store.next()


async def process_price(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
            data['price'] = message.text
    await message.answer('photo of prod?')
    await Store.next()


async def process_photo(message:types.Message,state:FSMContext):
    photo= message.photo[-1].file_id
    async with state.proxy() as data:
        await message.answer_photo(
            photo=photo,
            caption=f"{data['name']}\n{data['size']}\n{data['cat']}\n{data['price']}"
        )
    await state.finish()



def register_store(dp:Dispatcher):
    dp.register_message_handler(start_fsm,commands=['store'])
    dp.register_message_handler(process_name,state=Store.name)
    dp.register_message_handler(process_size,state=Store.size)
    dp.register_message_handler(process_cat,state=Store.category)
    dp.register_message_handler(process_price,state=Store.price)
    dp.register_message_handler(process_photo,state=Store.photo,content_types=['photo'])