import sqlite3

connect = sqlite3.connect('telegram_base.db')
cursor = connect.cursor()


#print(cursor.execute("SELECT * FROM profiles ").fetchone())
print(782697565 in cursor.execute("SELECT profile_id FROM profiles WHERE super_user = 'true' ").fetchone())