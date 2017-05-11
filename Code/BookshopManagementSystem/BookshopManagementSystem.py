# -*- coding: utf-8 -*-


# all the imports
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'BookshopManagementSystem.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='pass'
))


app.config.from_envvar('BOOKSHOPMANAGEMENTSYSTEM_SETTINGS', silent=True)


def connect_db():
    """Connect to the specific database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the current application context"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database again at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html', session=session)


@app.route('/show_books')
def show_books():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    cur = db.execute('select bookid, title, author, inventory, salenum, bid, price, description from books order by id desc')
    entries = cur.fetchall()
    return render_template('show_books.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    #print(request.form.get('BookID'))
    #print(request.form.get('BookTitle'))
    #print(request.form.get('BookAuthor'))
    #print(request.form.get('Inventory'))
    #print(request.form.get('SaleNum'))
    #print(request.form.get('Bid'))
    #print(request.form.get('Price'))
    #print(request.form.get('Text'))
    db.execute('INSERT INTO books(bookid, title, author, inventory, salenum, bid, price, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',[request.form.get('BookID'), request.form.get('BookTitle'), request.form.get('BookAuthor'), request.form.get('Inventory'), request.form.get('SaleNum'), request.form.get('Bid'), request.form.get('Price'), request.form.get('Text')])
    db.commit()
    flash('New Book was successfully posted')
    return redirect(url_for('show_books'))


@app.route('/add_books')
def add_books():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    return render_template('add_books.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if session.get('logged_in'):
        return redirect(url_for('show_books'))
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('登录成功!')
            return redirect(url_for('show_books'))
    return render_template('signin.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        return redirect(url_for('show_entries'))
    return render_template('signup.html', error=error)


@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    flash('您已经安全退出!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
