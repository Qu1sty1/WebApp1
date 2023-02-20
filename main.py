from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3

conn = sqlite3.connect('server.db', check_same_thread=False)
sql = conn.cursor()
conn.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS routes (
   route TEXT,
   route_time INT,   
   route_length INT
)""")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zyxw4342vut123srqpo89nmlkjihgf78213123edc1233ba'

user = {'name': 'your name'}


@app.route('/')
def index():
    session['name'] = ''
    session['login'] = 0
    return "index"


@app.route('/about')
def about():
    return render_template('site_back.html', user=session['name'])


@app.route('/profile')
def profile():
    return "profile"


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if 'login' in session and session['login'] == 1:
        return redirect('/about')
    if request.method == 'GET':
        return render_template('login2.html')
    else:
        if request.form['login'] not in sql.execute(f"SELECT * FROM users").fetchall()[1]:
            sql.execute(f"""INSERT INTO users (login, password)
                                       VALUES('{request.form['login']}', '{request.form['password']}')""")
            flash('Succesfully!')
            conn.commit()
            return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def log():
    if 'login' in session and session['login'] == 1:
        return redirect('/about')
    if request.method == 'GET':
        return render_template('login.html')
    else:
        a = sql.execute(f"SELECT password FROM users WHERE login='{request.form['login']}'").fetchone()
        print(a)
        if a and a[0] == request.form['password']:
            session['login'] = 1
            session['name'] = request.form['login']
            flash('Succesfully!')
            return redirect('/about')
        else:
            flash('Invalid login or password')


if __name__ == '__main__':
    app.run(debug=True)