from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'posts.json'


def load_posts():
    """Загружает посты из JSON-файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_posts(posts):
    """Сохраняет посты в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Получить список всех постов."""
    return jsonify(load_posts())


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Создать новый пост."""
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title и content обязательны'}), 400

    posts = load_posts()
    new_post = {
        'id': len(posts) + 1,
        'title': data['title'],
        'content': data['content']
    }
    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Получить пост по ID."""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return jsonify({'error': 'Пост не найден'}), 404
    return jsonify(post)


if name == '__main__':
    app.run(debug=True)