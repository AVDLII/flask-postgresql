import psycopg2
from flask import Flask,render_template, request, redirect, url_for


app = Flask(__name__)


def db_conn():
    conn = psycopg2.connect(database="flask_db", host="192.168.122.118", user="postgres", password="psql", port="5432")
    return conn


@app.route('/')
def index():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM shopping_list;''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', data=data)


@app.route('/create', methods=['POST'])
def create():
    conn = db_conn()
    cursor = conn.cursor()

    item = request.form['item']
    price = request.form['price']
    quantity = request.form['quantity']

    cursor.execute('''INSERT INTO shopping_list (item, price, quantity) VALUES (%s, %s, %s);''',(item, price, quantity))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cursor = conn.cursor()

    item = request.form['item']
    price = request.form['price']
    quantity = request.form['quantity']
    id = request.form['id']

    cursor.execute('''UPDATE shopping_list SET item=%s, price=%s, quantity=%s WHERE id=%s;''', (item, price, quantity, id))

    conn.commit()
    cursor.close()
    conn.close

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cursor = conn.cursor()

    id = request.form['id']

    cursor.execute('''DELETE FROM shopping_list WHERE id=%s;''', (id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))
