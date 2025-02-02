from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

add_user_data = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🆕Добавить данные'),
                                               KeyboardButton(text='👁️Просмотр данных'), ],
                                              [KeyboardButton(text='✨Пожелания'),
                                               KeyboardButton(text='🥂Тост'), ],
                                              [KeyboardButton(text='🎁Открытки'),
                                               KeyboardButton(text='❌Отмена'), ],
                                              [KeyboardButton(text='🗑️Удалить данные'),
                                               KeyboardButton(text='✏️Редактировать')]], resize_keyboard=True)

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🗑️Удалить по ID'),
                                       KeyboardButton(text='Удалить данные'), ],
                                      [KeyboardButton(text='Данные по ID'),
                                       KeyboardButton(text='❌Отмена')],
                                      [KeyboardButton(text='Объявление'),
                                       KeyboardButton(text='Картинка')]], resize_keyboard=True)

edit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фамилия', callback_data='surname'),
     InlineKeyboardButton(text='Имя', callback_data='name'),
     InlineKeyboardButton(text='Дата', callback_data='date')], ], resize_keyboard=True)

# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
#                                                            request_contact=True)]],
#                                  resize_keyboard=True)
