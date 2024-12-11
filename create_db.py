import sqlite3

conn = sqlite3.connect('users.db')
conn.execute('''
CREATE TABLE log_module (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    FOREIGN KEY (log_id) REFERENCES logs (id),
    FOREIGN KEY (module_id) REFERENCES modules (id)
);

''')
conn.commit()
conn.close()
