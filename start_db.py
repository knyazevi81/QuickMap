import sqlite3


def main():
    connect = sqlite3.connect('telegram_base.db')
    cursor = connect.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles(
    id INTEGER PRIMARY KEY,
    profile_id INTEGER,
    profile_username TEXT,
    activity TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    profile_id INTEGER,
    type_todo INTEGER,
    task TEXT,
    data TEXT
    )
    ''')

    connect.commit()
    connect.close()


if __name__ == '__main__':
    main()
    print('The database was created successfully ')
