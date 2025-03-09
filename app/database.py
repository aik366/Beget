import asyncio
import aiosqlite
from datetime import date, datetime, timedelta
from pathlib import Path

PATH_DB = Path(__file__).parent.parent / 'DATA' / 'user.db'

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


async def calculate_age(born):
    day, month, year = map(int, born.split('.'))
    born = datetime(year, month, day)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


async def get_age_suffix(age: int) -> str:
    if 11 <= age % 100 <= 14:
        return "лет"
    last_digit = age % 10
    if last_digit == 1:
        return "год"
    if 2 <= last_digit <= 4:
        return "года"
    return "лет"


async def create_table_users():
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "tg_id BIGINT, full_name TEXT, id_data TEXT)")


async def create_table_note():
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "tg_id BIGINT, note_name TEXT, note_text TEXT, note_data TEXT, note_type TEXT, file_id TEXT)")


async def create_table_birthday():
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS birthday (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "tg_id BIGINT, surname TEXT, name TEXT, data TEXT, delta_time INTEGER, age INTEGER)")


async def add_column():
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("ALTER TABLE users ADD file_id TEXT")


async def start_db(tg_id, full_name, id_data=my_time):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT * FROM users WHERE tg_id == ?", (tg_id,))
        data = await cursor.fetchone()
        if not data:
            await db.execute("INSERT INTO users (tg_id, full_name, id_data) VALUES (?, ?, ?)",
                             (tg_id, full_name, id_data))
            await db.commit()


async def add_db(tg_id, surname, name, data):
    split_data = data.split('.')
    data_get = await get_data(split_data[0], split_data[1])
    data_age = await calculate_age(data)
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("INSERT INTO birthday (tg_id, surname, name, data, delta_time, age) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (tg_id, surname.capitalize(), name.capitalize(), data, data_get, data_age))
        await db.commit()


async def db_check(surname, name):
    surname, name = surname.capitalize(), name.capitalize()
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT * FROM birthday WHERE surname == ? AND name == ?",
                                  (surname, name))
        return await cursor.fetchone()


async def update_surname(new_surname, surname, name):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("UPDATE birthday SET surname = ? WHERE surname = ? AND name = ?", (new_surname, surname, name))
        await db.commit()


async def update_name(new_name, surname, name):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("UPDATE birthday SET name = ? WHERE surname = ? AND name = ?", (new_name, surname, name))
        await db.commit()


async def update_data(new_data, surname, name):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("UPDATE birthday SET data = ? WHERE surname = ? AND name = ?", (new_data, surname, name))
        await db.commit()
        await delta_db(db)


async def delta_db(e):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT surname, name, data FROM birthday")
        users = await cursor.fetchall()
        for el in users:
            tmp = str(el[2]).split('.')
            data_get = await get_data(tmp[0], tmp[1])
            data_age = await calculate_age(el[2])
            await db.execute("UPDATE birthday SET delta_time = ?, age = ? WHERE surname = ? AND name = ?",
                             (data_get, data_age, el[0], el[1]))
        await db.commit()


async def db_select():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT surname, name, delta_time, age FROM birthday ORDER BY delta_time ASC")
        users = await cursor.fetchall()
        data_txt = ""
        for el in users:
            data_txt += f"{el[0]} {el[1]} - {el[3]} {await get_age_suffix(el[3])}, до ДР: {el[2]} дней\n"
        return data_txt


async def select_data():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT surname, name, data FROM birthday ORDER BY delta_time ASC")
        users = await cursor.fetchall()
        data_txt = ""
        for el in users:
            data_txt += f"{el[0]} {el[1]} - {el[2]}\n"
        return data_txt


async def db_select_id():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT tg_id FROM users")
        users = await cursor.fetchall()
        return set(el[0] for el in users)


async def db_select_users():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT tg_id, full_name, id_data FROM users")
        users = await cursor.fetchall()
        return users


async def delete_select(tg_id):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT surname, name, data FROM birthday WHERE tg_id == ? ORDER BY delta_time ASC",
            (tg_id,))
        users = await cursor.fetchall()
        data_txt = ""
        for num, el in enumerate(users, 1):
            data_txt += f"{num} - {el[0]} {el[1]} {el[2]}\n"
        return data_txt


async def delete_to_number(tg_id, number):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT surname, name FROM birthday WHERE tg_id == ? ORDER BY delta_time ASC",
            (tg_id,))
        users = await cursor.fetchall()
        data_dict = {}
        for num, el in enumerate(users, 1):
            data_dict[num] = [el[0], el[1]]
        surname, name = data_dict[number]
        async with aiosqlite.connect(PATH_DB) as db:
            await db.execute("DELETE FROM birthday WHERE surname = ? AND name = ?", (surname, name))
            await db.commit()


async def edit_to_number(tg_id, number):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT surname, name, data FROM birthday WHERE tg_id == ? ORDER BY delta_time ASC",
            (tg_id,))
        users = await cursor.fetchall()
        data_dict = {}
        for num, el in enumerate(users, 1):
            data_dict[num] = [el[0], el[1], el[2]]
        return data_dict[number]


async def admin_delete(surname, name):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("DELETE FROM birthday WHERE surname = ? AND name = ?", (surname, name))
        await db.commit()


async def db_delete_id(tg_id):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
        await db.commit()


async def birthday_reminder():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT surname, name FROM birthday WHERE delta_time = ?", (3,))
        users = await cursor.fetchall()
        if users:
            data_txt = "Через 3 дня у\n"
            for el in users:
                data_txt += f"{el[0]} {el[1]}\nдень рождения!!!\nне забудьте поздравить!\n"
            return data_txt
        return "none"


async def birthday():
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute("SELECT surname, name FROM birthday WHERE delta_time = ?", (0,))
        users = await cursor.fetchall()
        if users:
            data_txt = "Сегодня у\n"
            for el in users:
                data_txt += f"{el[0]} {el[1]}\nдень рождения!!!\nне забудьте поздравить!\n"
            return data_txt
        return "none"


async def add_note(tg_id, note_name, note_text=None, note_type=None, file_id=None):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("INSERT INTO notes (tg_id, note_name, note_text, note_data, note_type, file_id) "
                         "VALUES (?, ?, ?, ?, ?, ?)",
                         (tg_id, note_name, note_text, my_time, note_type, file_id))
        await db.commit()


async def update_note_name(tg_id, new_name, note_name, note_text):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("UPDATE notes SET note_name = ? WHERE tg_id = ? AND note_name = ? AND note_text = ?",
                         (new_name, tg_id, note_name, note_text))
        await db.commit()


async def update_note_text(tg_id, new_text, note_name, note_text):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("UPDATE notes SET note_text = ? WHERE tg_id = ? AND note_name = ? AND note_text = ?",
                         (new_text, tg_id, note_name, note_text))
        await db.commit()


async def select_note(tg_id):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT note_name, note_text, note_type, file_id FROM notes WHERE tg_id == ?",
            (tg_id,))
        users = await cursor.fetchall()
        data_dict = {}
        for num, el in enumerate(users, 1):
            data_dict[num] = [el[0], el[1], el[2], el[3]]
        return data_dict


async def note_delete(tg_id, note_name, note_text):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("DELETE FROM notes WHERE tg_id = ? AND note_name = ? AND note_text = ?",
                         (tg_id, note_name, note_text))
        await db.commit()


async def edit_note_text(tg_id, number):
    async with aiosqlite.connect(PATH_DB) as db:
        cursor = await db.execute(
            "SELECT note_text, note_data FROM notes WHERE tg_id == ? ORDER BY note_data ASC",
            (tg_id,))
        users = await cursor.fetchall()
        data_dict = {}
        for num, el in enumerate(users, 1):
            data_dict[num] = [el[0], el[1]]
        return data_dict[number]


if __name__ == '__main__':
    pass
    print(PATH_DB)
    # asyncio.run(create_table_users())
    # print(asyncio.run(add_note_text(428030603, "note_text_3")))
    # print(asyncio.run(select_note(428030603)))
    # print(asyncio.run(edit_note_text(428030603, 3)))
    # asyncio.run(add_column())
    # asyncio.run(add_db("Галстян Айк 22.04.1972"))
    # asyncio.run(update_surname("Галстян", "Погосян", "Айк"))
    # asyncio.run(delta_db(''))
    print(asyncio.run(db_select()))
    # print(asyncio.run(start_db(1338196844, 'LA')))
    # print(asyncio.run(get_data('19', '01')))
    # print(calculate_age('22.04.1972'))
