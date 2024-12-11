import sqlite3


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # ایجاد جدول users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # ایجاد جدول logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            user_id TEXT NOT NULL,
            user_agent TEXT NOT NULL,
            browser_name TEXT NOT NULL,
            browser_version TEXT NOT NULL,
            platform TEXT NOT NULL,
            plugins TEXT NOT NULL,
            country TEXT NOT NULL
        )
    ''')

    # ایجاد جدول js_commands
    c.execute('''
        CREATE TABLE IF NOT EXISTS js_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            command TEXT NOT NULL
        )
    ''')

    # ایجاد جدول modules
    c.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL
        )
    ''')

    # ایجاد جدول log_module برای ارتباط بین لاگ‌ها و ماژول‌ها
    c.execute('''
        CREATE TABLE IF NOT EXISTS log_module (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            FOREIGN KEY (log_id) REFERENCES logs (id),
            FOREIGN KEY (module_id) REFERENCES modules (id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
