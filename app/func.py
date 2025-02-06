from datetime import datetime

from aiogram import Bot
from app.database import birthday, birthday_reminder, db_select_id
import requests
from bs4 import BeautifulSoup
from config import API_KEY


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


async def get_weather_forecast(api_key=API_KEY, city="Krasnodar", days=5):
    # Запрос к API
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # для получения данных в °C
        "lang": "ru"  # перевод описания на русский
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки
        data = response.json()

        # Группировка данных по дням
        forecasts = {}
        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            if date not in forecasts:
                forecasts[date] = []
            forecasts[date].append(item)

        # Выборка данных на указанное количество дней
        selected_dates = sorted(forecasts.keys())[:days]
        result = []
        for date in selected_dates:
            day_data = forecasts[date]
            # Пример агрегации данных (можно выбрать среднее или пиковые значения)
            temp_min = min(f["main"]["temp_min"] for f in day_data)
            temp_max = max(f["main"]["temp_max"] for f in day_data)
            description = day_data[0]["weather"][0]["description"]  # берем первое описание

            result.append({
                "date": date,
                "temp_min": temp_min,
                "temp_max": temp_max,
                "description": description,
                "humidity": day_data[0]["main"]["humidity"]
            })
        if result:
            date_txt = "Прогноз погоды в\nКраснодаре на 5 дней:\n---\n"
            for day in result:
                day_split = day['date'].split("-")
                date_txt += f"{day_split[2]}.{day_split[1]}.{day_split[0]}:\n"
                date_txt += f"от {day['temp_min']}°C до {day['temp_max']}°C\n"
                date_txt += f"{day['description'].capitalize()}\n"
                date_txt += f"---\n"

            return date_txt[:-4]

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


async def anekdot(bot: Bot):
    url = "https://anekdotov.net/anekdot/day/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        anekdot_block = soup.find('div', class_='anekdot')
        if anekdot_block:
            anekdot_text = anekdot_block.get_text(strip=True)
            for bot_id in await db_select_id():
                await bot.send_message(bot_id, f'Анекдот дня:\n{anekdot_text}\n\n{await get_weather_forecast()}')


if __name__ == '__main__':
    pass
