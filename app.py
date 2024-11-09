from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'userdata'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


def is_user_registered(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None


@app.route('/', methods=['GET', 'POST'])
def page_a():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return "错误: 用户名为空."
        if not is_user_registered(username):
            return "错误: 用户未注册."
        return redirect(url_for('page_b', username=username))
    return render_template('page_a.html')


@app.route('/page_b/<username>')
def page_b(username):
    return render_template('page_b.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)