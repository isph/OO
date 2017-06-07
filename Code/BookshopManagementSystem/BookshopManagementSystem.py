# -*- coding: utf-8 -*-


# all the imports
import os
import System
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


global S


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
    if session.get('logged_in') and S.ac.get_account()!=None:
        return redirect(url_for('show_books'))
    return render_template('index.html')


@app.route('/show_books')
def show_books():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    cur = db.execute('select * from books order by id desc')
    entries = cur.fetchall()
    accounttype = S.ac.get_account().username
    #for entry in entries:
    #    for e in entry:
    #        print(e)
    return render_template('show_books.html', entries=entries, accounttype=accounttype)


@app.route('/add_sof', methods=['GET', 'POST'])
def add_sof():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    if request.method=='POST':
        db = get_db()
        db.execute('INSERT INTO orderform(type, bookname, booknum, fixprice, bidprice) VALUES (?,?,?,?,?)',['1',request.form.get('BookName'),request.form.get('BookNum'),request.form.get('fixPrice'),request.form.get('Bid')])
        db.commit()
    return render_template('success.html')


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    db.execute('INSERT INTO books(bookid, title, author, inventory, salenum, bid, price, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',[request.form.get('BookID'), request.form.get('BookTitle'), request.form.get('BookAuthor'), request.form.get('Inventory'), request.form.get('SaleNum'), request.form.get('Bid'), request.form.get('Price'), request.form.get('Text')])
    db.commit()
    flash('New Book was successfully posted')
    return redirect(url_for('show_books'))


@app.route('/modify_books', methods=['POST'])
def modify_books():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    db.execute('update books \
      SET bookid=?, title=?, author=?, inventory=?, salenum=?, bid=?, price=?, description=? \
      WHERE bookid=?',\
      [request.form.get('BookID'), request.form.get('BookTitle'), request.form.get('BookAuthor'), request.form.get('Inventory'), request.form.get('SaleNum'), request.form.get('Bid'), request.form.get('Price'), request.form.get('Text'),request.form.get('BookID')])
    db.commit()
    return redirect(url_for('show_books'))


@app.route('/add_books')
def add_books():
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    return render_template('add_books.html')


@app.route('/show_aof')
def show_aof():
    db = get_db()
    cur = db.execute('SELECT * FROM orderform WHERE type=1')
    aoflist = cur.fetchall()
    return render_template('show_aof.html', aoflist=aoflist)


@app.route('/deal_apply', methods=['GET', 'POST'])
def deal_apply():
    if request.method == 'POST':
        deal = request.form['deal_apply']
        isbn = request.form['isbn']
        db = get_db()
        if deal=='reject' or deal == 'receive':
            db.execute('DELETE FROM orderform WHERE phone=?',[isbn])
            db.commit()
            cur = db.execute('SELECT * from orderform WHERE type=4')
            reserve_list = cur.fetchall()
            return render_template('reserve_list.html', reserve_list=reserve_list)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        db = get_db()
        if (request.form['username'] == app.config['USERNAME']) and (request.form['password'] == app.config['PASSWORD']):
            session['logged_in'] = True
            cur = db.execute('SELECT username, password, money from account WHERE username="admin"')
            accountList = cur.fetchall()
            account = accountList[0]
            S.ac.new_account('1')
            S.ac.get_account().set_username(account["username"])
            S.ac.get_account().set_password(account["password"])
            S.ac.get_account().set_money(account["money"])
            S.ac.get_account().set_type('1')
            cur = db.execute('SELECT * from orderform WHERE type=4')
            reserve_list = cur.fetchall()
            if len(reserve_list) != 0:
                return render_template('reserve_list.html', reserve_list=reserve_list)
            return redirect(url_for('show_books'))
        elif (request.form['username'] == 'customer') and (request.form['password'] == 'pass'):  # 顾客登录
            session['logged_in'] = True
            cur = db.execute('SELECT username, password, money from account WHERE username="customer"')
            accountList = cur.fetchall()
            account = accountList[0]
            S.ac.new_account('2')
            S.ac.get_account().set_username(account["username"])
            S.ac.get_account().set_password(account["password"])
            S.ac.get_account().set_money(account['money'])
            S.ac.get_account().set_type('2')
            return redirect(url_for('show_books'))
        elif (request.form['username'] == 'supplier') and (request.form['password'] == 'pass'):  # 供货商登录
            session['logged_in'] = True
            cur = db.execute('SELECT username, password, money from account WHERE username="supplier"')
            accountList = cur.fetchall()
            account = accountList[0]
            S.ac.new_account('3')
            S.ac.get_account().set_username(account["username"])
            S.ac.get_account().set_password(account["password"])
            S.ac.get_account().set_money(account["money"])
            S.ac.get_account().set_type('3')
            return redirect(url_for('sof_list'))
        else:
            error = 'Invalid UserName or Password!'
    return render_template('signin.html', error=error)


@app.route('/sof_list')
def sof_list():
    error = None
    if not session.get('logged_in'):
        return redirect(url_for('signin'))
    db = get_db()
    cur = db.execute('SELECT * from orderform WHERE type="1"')
    sofs = cur.fetchall()
    return render_template('sof_list.html', sofs=sofs)


@app.route('/cancel_aof', methods=['GET', 'POST'])
def cancel_aof():
    if request.method=='POST' and request.form['cancel_aof']=='cancel':
        db = get_db()
        db.execute('DELETE FROM orderform WHERE type="1" AND backup=?',[request.form['isbn']])
        db.commit()
        return redirect(url_for('show_aof'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        return redirect(url_for('show_entries'))
    return render_template('signup.html', error=error)


@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    #db = get_db()
    #db.execute('UPDATE account SET money=? WHERE username=?', [S.ac.get_account().get_money(), S.ac.get_account().get_username()])
    flash('您已经安全退出!')
    return redirect(url_for('index'))


@app.route('/sale_strategy', methods=['GET','POST'])
def sale_strategy():
    if request.method == 'POST' and request.form.get('BookID')=='-1':
        db = get_db()
        db.execute('UPDATE books SET discount=?, time=?, bundle=?, description=? WHERE bookid=?', [float(request.form.get('Discount')), float(request.form.get('Deadline')), request.form.get('BundleSale'), request.form.get('Description'),S.dc.text_1])
        db.commit()
        return redirect(url_for('show_books'))
    elif request.method == 'POST' and request.form.get('BookID')!='-1':
        S.dc.text_1 = request.form.get('BookID')
        #print(request.form.get('BookID'))
        #print('9999999999999999999')
    return render_template('sale_strategy.html')


@app.route('/cus_order', methods=['GET', 'POST'])
def customer_order_form():
    error = None
    if request.method == 'POST':
        cof = S.ofc.new_customer_orderform()
        cof.set_bookname(request.form.get('BookName'))
        cof.set_booknum(int(request.form.get('BookNum')))
        cof.set_phonenum(request.form.get('phone_number'))
        cof.set_cusname(request.form.get('Name'))
        cof.set_address(request.form.get('Address'))
        S.ac.get_account().set_money(float(S.ac.get_account().get_money()-10*cof.get_booknum()))
        money = S.ac.get_account().get_money()
        db = get_db()
        db.execute('UPDATE account SET money=? WHERE username="customer"', [money])
        db.commit()
        return render_template('success.html')
    return render_template('customer_order_form.html', error=error)


@app.route('/shop_order', methods=['GET', 'POST'])
def shopkeeper_order_form():
    error = None
    if request.method == 'POST':
        sof = S.ofc.new_shopkeeper_orderform()
        sof.set_bookname(request.form.get('BookName'))
        sof.set_booknum(int(request.form.get('BookNum')))

        S.ac.get_account().set_money(float(S.ac.get_account().get_money()-float(request.form.get('fixPrice'))*sof.get_booknum()))
        money = S.ac.get_account().get_money()
        db = get_db()
        db.execute('INSERT INTO orderform(type, backup, bookname, booknum, fixprice, bidprice) VALUES (?,?,?,?,?,?)',['1',request.form['ISBN'], request.form.get('BookName'),request.form.get('BookNum'),request.form.get('fixPrice'),request.form.get('Bid')])
        #db.commit()
        db.execute('UPDATE account SET money=? WHERE username="admin"', [money])
        db.commit()
        return redirect(url_for('show_books'))
    return render_template('shopkeeper_order_form.html')


@app.route('/personal_info')
def personal_info():
    account = S.ac.get_account()
    return render_template('personal_info.html', account=account)


@app.route('/del_book', methods=['GET', 'POST'])
def del_book():
    error = None
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        db = get_db()
        db.execute('DELETE from books WHERE bookid=?',[book_id])
        db.commit()
        print("Delete!")
        return redirect(url_for('show_books'))
    return render_template('del_book.html')


@app.route('/search_books', methods=['GET','POST'])
def search_books():
    if request.method == 'POST':
        bookname = request.form.get('bookname')
        db = get_db()
        if request.form['options'] == '书名':
            cur = db.execute('SELECT * from books WHERE title=?', [bookname])
        elif request.form['options'] == '书号':
            cur = db.execute('SELECT * from books WHERE bookid=?', [bookname])
        else:
            pass
        booklist = cur.fetchall()
        return render_template('search_books.html', booklist=booklist)
    return render_template('search_books.html')


@app.route('/reserve_books', methods=['GET','POST'])
def reserve_books():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO orderform(type,bookname,name,phone,address) VALUES (?,?,?,?,?)',['4',request.form.get('BookName'),request.form.get('Author'),request.form.get('ISBN'),'customer'])
        db.commit()
        return render_template('success.html')
    return render_template('reserve_books.html')


if __name__ == '__main__':
    S = System.System()
    app.run()
