from aiogram import Bot
from app.database import birthday, birthday_reminder, db_select_id


async def open_birthday(bot: Bot):
    func_txt = await birthday()
    if func_txt != "none":
        for bot_id in await db_select_id():
            await bot.send_message(bot_id, f'{func_txt}')


async def open_birthday_reminder(bot: Bot):
    func_txt = await birthday_reminder()
    if func_txt != "none":
        for bot_id in await db_select_id():
            await bot.send_message(bot_id, f'{func_txt}')


if __name__ == '__main__':
    pass
