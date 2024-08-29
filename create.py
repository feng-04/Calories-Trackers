import sqlite3


con = sqlite3.connect("database.db")
cursor = con.cursor()




cursor.execute('''
             CREATE TABLE IF NOT EXISTS date(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             date TEXT NOT NULL,
             calories TEXT NOT NULL, 
             people_id INTEGER, 
             FOREIGN KEY(people_id) REFERENCES people(id)
             )



'''
)

cursor.execute('''
                CREATE TABLE IF NOT EXISTS meals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                date TEXT NOT NULL, 
                amount REAL, 
                calories REAL,
                people_id INTEGER,
                FOREIGN KEY(people_id) REFERENCES people(id)
                )'''
              )
    
cursor.execute('''
                CREATE TABLE IF NOT EXISTS People(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                password INTEGER, 
                height REAL, 
                weight REAL, 
                age REAL, 
                calories REAL
                )'''
               )
    