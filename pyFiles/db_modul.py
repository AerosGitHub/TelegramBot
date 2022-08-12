import sqlite3


def get_all_inf_from_db():
    connect = sqlite3.connect('Database/weather_data.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()


def add_inf_in_db(db_inf: tuple):
    connect = sqlite3.connect('Database/weather_data.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?);", db_inf)
    connect.commit()


def delete_inf_from_db(num):
    connect = sqlite3.connect('Database/weather_data.db')
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM users WHERE userid='{num}';")
    connect.commit()
