from aiogram import Bot
from app.database import birthday, birthday_reminder, db_select_id
import requests
from bs4 import BeautifulSoup


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


async def anekdot(bot: Bot):
    url = "https://anekdotov.net/anekdot/day/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        anekdot_block = soup.find('div', class_='anekdot')
        if anekdot_block:
            anekdot_text = anekdot_block.get_text(strip=True)
            for bot_id in await db_select_id():
                await bot.send_message(bot_id, f'Анекдот дня:\n{anekdot_text}')


if __name__ == '__main__':
    pass
