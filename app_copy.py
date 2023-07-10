from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# MySQL connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'DB_TEST'

@app.route('/')
def order():
    return render_template('submit_menu.html')

@app.route('/submit_menu', methods=['POST'])
def submit_menu():
    number = request.form['number']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    # Create MySQL connection
    mysql = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        autocommit=True
    )

    # Create MySQL cursor
    cursor = mysql.cursor()

    # Execute insert query
    query = "INSERT INTO menus_v2 (number, name, price, quantity) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (number, name, price, quantity))

    # Close cursor and MySQL connection
    cursor.close()
    mysql.close()

    return f"연번: {number}, 메뉴: {name}, 가격: {price}, 수량: {quantity} 주문이 완료되었습니다."

@app.route('/result')
def result():
    # Create MySQL connection
    mysql = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        autocommit=True
    )

    # Create MySQL cursor
    cursor = mysql.cursor()

    cursor.execute("SELECT * FROM menus_v2")
    data = cursor.fetchall()

    # Close cursor and MySQL connection
    cursor.close()
    mysql.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800)
