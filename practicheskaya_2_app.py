from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Для flash-сообщений
DATA_FILE = 'users.json'


def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_user(user):
    users = load_users()
    users.append(user)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if len(password) < 8:
            flash('Пароль должен содержать минимум 8 символов', 'danger')
            return redirect(url_for('register'))

        user = {'name': name, 'email': email, 'password': password}
        save_user(user)
        return render_template('result.html', user=user)

    return render_template('register.html')


@app.route('/users')
def users():
    return jsonify(load_users())


if name == '__main__':
    app.run(debug=True)