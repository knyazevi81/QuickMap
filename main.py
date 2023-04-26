import sqlite3
import time
from modules.parsing_tasks import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import config
import datetime

connect = sqlite3.connect('telegram_base.db')
cursor = connect.cursor()

bot = Bot(config.tele_token)
dp = Dispatcher(bot)

# Инлайн клавиатура
keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Зарегистрироваться', callback_data='up_profile'))
menu_board = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Вернуться в меню', callback_data='menu'))

# Кнопки
menu_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/menu'))

last_message = []
last_profile = []
last_username = []


@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    prompt = ''
    all_reg_id = cursor.execute('SELECT profile_id FROM profiles').fetchall()
    all_tasks_id = cursor.execute(f'''SELECT type_todo, id, task
                                      FROM tasks WHERE profile_id = {message.from_user.id}
                                      AND (type_todo = 1 OR type_todo = 0)
                                      ORDER BY type_todo DESc''').fetchall()
    if not all_tasks_id:
        prompt = 'Активных задач на сегодня нет'
    else:
        emoji_todo = {1: '🟨', 0: '🟥'}
        for task in all_tasks_id:
            prompt += f'{emoji_todo[task[0]]}#[{task[1]}]:  {task[2]}\n'

    if user_in_db(message.from_user.id, all_reg_id):
        await message.reply_photo(photo=open('images/title.png', 'rb'),
                                  caption=f"👤Привет {message.from_user.username}\n"
                                          f"На {str(datetime.date.today())[5:10]} у вас:\n"
                                          f"🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧\n"
                                          f"{prompt}\n"
                                          f"🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧\n",
                                  reply_markup=menu_button)
    else:
        await bot.send_message(message.from_user.id, f'🌝Привет {message.from_user.username}\n'
                                                     f'🚧Для того чтобы начать пользоваться бо'
                                                     f"том нажми 'зарегистрироваться'", reply_markup=keyboard)
        last_message.append(message.message_id + 1)
        last_profile.append(message.from_user.id)
        last_username.append(message.from_user.username)


@dp.callback_query_handler(text="up_profile")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=last_message[-1], chat_id=last_profile[-1], text='🎉Вы успешно зарегистри'
                                                                                            'ровались в базе данных!\n'
                                                                                            'Нажмите на кнопку /menu '
                                                                                            'чтобы попасть на главную'
                                                                                            ' страницу')
    data = (int(last_profile[-1]), f'@{last_username[-1]}', 'false')
    cursor.execute('INSERT INTO profiles(profile_id, profile_username, activity) VALUES(?,?,?)', data)
    connect.commit()


'''
@dp.callback_query_handler(text="press_me")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('1')
'''

if __name__ == '__main__':
    executor.start_polling(dp)
    connect.close()
