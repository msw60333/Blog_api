from flask import Flask, jsonify, request 
import  sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/authors', methods=['GET'])
def get_authors():
    conn = get_db_connection()
    authors = conn.execute('SELECT * FROM authors').fetchall()
    conn.close()
    
    return jsonify([dict(author) for author in authors])

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    author_id = request.args.get('author_id')
    if author_id:
        posts = conn.execute('SELECT * FROM posts WHERE author_id = ?', (author_id,)).fetchall()
    else:
        posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    
    return jsonify([dict(post) for post in posts])

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db_connection()

    post = conn.execute('''
        SELECT posts.id,posts.title,posts.content,posts.author_id,
            authors.id AS author_id,authors.name AS author_name,authors.bio AS author_bio
        FROM posts JOIN authors ON posts.author_id = authors.id WHERE posts.id = ?''', (id,)).fetchone()

    conn.close()

    if post is None:
        return jsonify({'error': 'Пост не найден'}), 404

    result = {
        'id': post['id'],
        'title': post['title'],
        'content': post['content'],
        'author_id': post['author_id'],
        'author': {
            'id': post['author_id'],
            'name': post['author_name'],
            'bio': post['author_bio']
        }
    }

    return jsonify(result)


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')
    
    if not title in data or not content in data or not author_id in data:
        return jsonify({'error': 'Проверьте введенные данные'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)',
                   (title, content, author_id))
    
    author = conn.execute('SELECT * FROM authors WHERE id = ?', (author_id,)).fetchone()
    if author is None:
        conn.close()
        return jsonify({'error': 'Автор не найден'}), 404
    
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    
    post = cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    return jsonify(dict(post)), 201


@app.route ('/authors/<int:id>/posts', methods=['GET'])
def get_author_posts(id):
    conn = get_db_connection()
    author = conn.execute('SELECT * FROM authors WHERE id = ?', (id,)).fetchone()

    if author is None:
        conn.close()
        return jsonify({'error': 'токого автора нету'}), 404

    posts = conn.execute('SELECT * FROM posts WHERE author_id = ?', (id,)).fetchall()
    conn.close()

    return jsonify([dict(post) for post in posts])


@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    conn = get_db_connection ()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if post == None :
        conn.close()
        return jsonify ({'error': 'такого поста нету' })
    
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Пост удален успешно'})


if __name__ == '__main__':
    app.run(debug=True)
    
    