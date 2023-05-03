import sqlite3
import time
import os
from modules.parsing_tasks import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
import config
import datetime

connect = sqlite3.connect(os.path.join(os.getcwd(), 'telegram_base.db'))
cursor = connect.cursor()

bot = Bot(config.tele_token)
dp = Dispatcher(bot)


def main_keyboard(user_id: int):
    admin_prof = cursor.execute(f"SELECT profile_id FROM profiles WHERE super_user='true'").fetchone()
    try:
        if user_id in admin_prof:
            return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='добавить задачу',
                                                                          callback_data='add_task'),
                                                         InlineKeyboardButton(text='увидеть все задания',
                                                                          callback_data='all_task'),
                                                         InlineKeyboardButton(text='создать команду',
                                                                          callback_data='all_task'),
                                                         )
    except:
        return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='добавить задачу',
                                                                          callback_data='add_task'),
                                                     InlineKeyboardButton(text='увидеть все задания',
                                                                          callback_data='all_task'))


def registration():
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='Зарегистрироваться', callback_data='up_profile'))


add_task = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='добавить задачу', callback_data='add_task'),
                                                 InlineKeyboardButton(text='увидеть все задания', callback_data='all_task'),
                                                 InlineKeyboardButton(text='Зарегистрироваться', callback_data='up_profile'))

# Кнопки
menu_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/menu'))

last_message = []
last_profile = []
last_username = []


# Основные хэндлер
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
            prompt += f'{emoji_todo[task[0]]}#[{task[1]}]: {task[2]}\n'

    if user_in_db(message.from_user.id, all_reg_id):
        await bot.send_message(message.from_user.id, f"👤Привет {message.from_user.username}\n"
                                                     f"На {str(datetime.date.today())[5:10]} у вас:\n"
                                                     f"-----------------------------------\n"
                                                     f"{prompt}\n"
                                                     f"-----------------------------------\n"
                                                     f"Ассисстент: {0}\n"
                                                     f"режим администратора: {0}",
                                                     reply_markup=main_keyboard(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f'🌝Привет {message.from_user.username}\n'
                                                     f'🚧Для того чтобы начать пользоваться бо'
                                                     f"том нажми зарегистрироваться ", reply_markup=registration())
        last_message.append(message.message_id + 1)
        last_profile.append(message.from_user.id)
        last_username.append(message.from_user.username)


@dp.message_handler()
async def start_menu(message: types.Message):
    if (message.text.split()[0]).lower() == 'admin' and message.text.split()[1] == config.admin_token:
        cursor.execute(f"UPDATE profiles SET super_user = ? WHERE profile_id = '{message.from_user.id}'", ('true',))
        await bot.send_message(message.from_user.id, '✅ Вы успешно активировали режим администратора')
    connect.commit()


# Инлайн хендрелы
@dp.callback_query_handler(text="up_profile")
async def send_random_value(callback: types.CallbackQuery):
    await bot.edit_message_text(message_id=last_message[-1], chat_id=last_profile[-1], text='🎉Вы успешно зарегистри'
                                                                                            'ровались в базе данных!\n'
                                                                                            'Нажмите на кнопку /menu '
                                                                                            'чтобы попасть на главную'
                                                                                            ' страницу')
    data = (int(last_profile[-1]), f'@{last_username[-1]}', 'false', 'false', 'noneteem')
    cursor.execute('INSERT INTO profiles(profile_id, profile_username, activity, super_user, teems) VALUES(?,?,?,?,?)', data)
    connect.commit()


'''
@dp.callback_query_handler(text="press_me")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('1')
'''

if __name__ == '__main__':
    executor.start_polling(dp)
    connect.close()
