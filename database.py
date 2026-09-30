import sqlite3

DB_NAME = 'blog.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT
        )''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS posts (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       content TEXT NOT NULL,
                       author_id INTEGER,
                       FOREIGN KEY (author_id) REFERENCES authors (id)
                   )''')
    
    conn.commit()
    conn.close()
    

def seed_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    authors = [
        ("Иван " , "Учитель технологии"),
        ("Алексей" , "Учитель математики"),
        ("Георгий", "ПУтешественник")
    ]
    
    cursor.executemany('INSERT INTO authors (name, bio) VALUES (?, ?)', authors)
    
    posts = [
        ("Путешествие в горы", "Сегодня я отправился в горы и увидел невероятные виды.", 1),
        ("Математика в повседневной жизни", "Математика окружает нас повсюду, даже в самых простых вещах.", 2),
        ("Советы для путешественников", "Если вы планируете путешествие, вот несколько советов, которые помогут вам подготовиться.", 3),
        ("Иновации в образовании", "Современные технологии меняют подход к обучению и преподаванию.", 1),
        ("Решение сложных задач", "Иногда решение сложной задачи требует нестандартного подхода и креативного мышления.", 2),
    ]
    
    cursor.executemany('INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)', posts)
    
    conn.commit()
    conn.close()    
    
if __name__ == "__main__":
    init_db()
    seed_db()
print ("База данных blog.db создана ")

