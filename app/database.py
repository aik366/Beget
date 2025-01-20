import asyncio
import aiosqlite
from datetime import date, datetime, timedelta

my_time = datetime.now().strftime("%d.%m.%Y")
data = datetime.now()
delta_days = data + timedelta(days=3)
data = str(data.strftime("%d-%m"))
delta_days = str(delta_days.strftime("%d-%m"))


async def get_data(day: str, month: str):
    day = int(day.lstrip('0'))
    month = int(month.lstrip('0'))
    teachers_day = date(datetime.now().year, month, day)
    today = date.today()
    if teachers_day >= today:
        return (teachers_day - today).days
    else:
        teachers_day = date(datetime.now().year + 1, month, day)
        return (teachers_day - today).days


async def create_table():
    async with aiosqlite.connect('../DATA/user.db') as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_id BIGINT, user_name TEXT, data_time TEXT)")
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users_data (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_surname TEXT, user_name TEXT, user_data TEXT, delta_time INTEGER)")


async def add_column():
    async with aiosqlite.connect('../DATA/user.db') as db:
        await db.execute("ALTER TABLE users_data ADD delta_time INTEGER")


async def start_db(us_id, us_name, us_time=my_time):
    async with aiosqlite.connect('DATA/user.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id == ?", (us_id,))
        data = await cursor.fetchone()
        if not data:
            await db.execute("INSERT INTO users (user_id, user_name, data_time) VALUES (?, ?, ?)",
                             (us_id, us_name, us_time))
            await db.commit()


async def add_db(user_text: str):
    user_split = user_text.split()
    split_data = user_split[2].replace(',', '.').split('.')
    data_get = await get_data(split_data[0], split_data[1])
    split_data = f"{split_data[0].zfill(2)}.{split_data[1].zfill(2)}.{split_data[2]}"
    # split_data = date.fromisoformat(split_data)
    async with aiosqlite.connect('DATA/user.db') as db:
        await db.execute("INSERT INTO users_data (user_surname, user_name, user_data, delta_time) VALUES (?, ?, ?, ?)",
                         (user_split[0], user_split[1], split_data, data_get))
        await db.commit()


async def db_update(us_id, us_surname):
    async with aiosqlite.connect('DATA/user.db') as db:
        await db.execute("UPDATE users SET user_surname = ? WHERE user_id = ?", (us_surname, us_id))
        await db.commit()


async def delta_db(e):
    async with aiosqlite.connect('DATA/user.db') as db:
        cursor = await db.execute("SELECT * FROM users_data")
        users = await cursor.fetchall()
        for el in users:
            tmp = str(el[3]).split('.')
            data_get = await get_data(tmp[0], tmp[1])
            await db.execute("UPDATE users_data SET delta_time = ? WHERE user_surname = ? AND user_name = ?",
                             (data_get, el[1], el[2]))
        await db.commit()


async def db_select():
    async with aiosqlite.connect('DATA/user.db') as db:
        # cursor = await db.execute("SELECT * FROM users_data ORDER BY strftime('%m.%d', user_data) ASC")
        cursor = await db.execute("SELECT * FROM users_data ORDER BY delta_time ASC")
        users = await cursor.fetchall()
        data_txt = ""
        for el in users:
            # tmp = str(el[3]).split('.')
            # # data_get = await get_data(tmp[2], tmp[1])
            # tmp = f"{tmp[2]}.{tmp[1]}.{tmp[0]}"
            data_txt += f"{el[1]} {el[2]} {el[3]} ({el[4]})\n"
        return data_txt


async def db_select_id():
    async with aiosqlite.connect('DATA/user.db') as db:
        cursor = await db.execute("SELECT user_id FROM users")
        users = await cursor.fetchall()
        return [el[0] for el in users]


async def db_select_users():
    async with aiosqlite.connect('DATA/user.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        data_txt = ""
        for el in users:
            data_txt += f"{el[1]} {el[2]} {el[3]}\n"
        return data_txt


async def db_data_delete(surname, name):
    async with aiosqlite.connect('DATA/user.db') as db:
        await db.execute("DELETE FROM users_data WHERE user_surname = ? AND user_name = ?", (surname, name))
        await db.commit()


async def birthday_reminder():
    async with aiosqlite.connect('DATA/user.db') as db:
        cursor = await db.execute("SELECT * FROM users_data WHERE delta_time = ?", (3,))
        users = await cursor.fetchall()
        if users:
            data_txt = "Через 3 дня у\n"
            for el in users:
                data_txt += f"{el[1]} {el[2]}\nдень рождения!!!\nне забудьте поздравить!\n"
            return data_txt
        return "none"


async def birthday():
    async with aiosqlite.connect('DATA/user.db') as db:
        # cursor = await db.execute("SELECT * FROM users_data WHERE strftime('%d-%m', user_data) = ?", (f'{data}',))
        cursor = await db.execute("SELECT * FROM users_data WHERE delta_time = ?", (0,))
        users = await cursor.fetchall()
        if users:
            data_txt = "Сегодня у\n"
            for el in users:
                data_txt += f"{el[1]} {el[2]}\nдень рождения!!!\nне забудьте поздравить!\n"
            return data_txt
        return "none"


if __name__ == '__main__':
    pass
    # print(my_time)
    # asyncio.run(create_table())
    # print(asyncio.run(delta_db()))
    # asyncio.run(add_column())
    # asyncio.run(add_db("Галстян Айк 22.04.1972"))
    # asyncio.run(db_update(428030603, 'Admin'))
    # print(asyncio.run(delta_db('')))
    print(asyncio.run(db_select()))
    # print(asyncio.run(db_check(5194830049, 'Ивано')))

    # print(asyncio.run(get_data('19', '01')))
