from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# MySQL connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'DB_TEST'

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

@app.route('/')
def first_page():
    return render_template('first_page.html')

@app.route('/order', methods=['POST'])
def order():
    cursor.execute("SELECT * FROM menus_v2")
    data = cursor.fetchall()
    return render_template('order.html', data=data)

@app.route('/add_menu', methods = ['POST'])
def add_menu():
    cursor.execute("SELECT * FROM menus_v2")
    data = cursor.fetchall()
    return render_template('add_menu.html', data = data)

@app.route('/submit_menu', methods=['POST'])
def submit_menu():
    try:
        number = int(request.form['number'])
        menu = str(request.form['menu'])
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
    except ValueError:
        return '잘못된 입력입니다. 메뉴는 문자, 수량은 숫자로 입력해주세요.'

    cursor.execute(f"INSERT INTO menus_v2 (number, name, price, quantity) VALUES ({number}, '{menu}', {price}, {quantity});")
    mysql.commit()
    return redirect('/result')

@app.route('/order/jihee', methods=['POST'])
def order_jihee():
    menu = str(request.form['menu'])
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        return '잘못된 입력입니다. 메뉴는 문자, 수량은 숫자로 입력해주세요.'

    if menu.isnumeric():
        return '잘못된 입력입니다. 메뉴는 문자, 수량은 숫자로 입력해주세요.'

    cursor.execute(f"SELECT * FROM menus_v2 WHERE name='{menu}';")
    res = cursor.fetchall()

    if len(res) == 0:
        return '주문하신 메뉴는 없는 메뉴입니다.'

    after_quantity = res[0][3] - quantity

    if quantity <= 0:
        error_message_1 = '수량은 1개 이상 주문해주세요.'
        return error_message_1
    elif after_quantity >= 0:
        cursor.execute(f"UPDATE menus_v2 SET quantity = {after_quantity} WHERE name = '{menu}';")
        mysql.commit()
        return redirect('/result')
    else:
        cursor.execute(f"SELECT quantity FROM menus_v2 WHERE name = '{menu}';")
        residual_quantity = cursor.fetchall()
        quantity_data = residual_quantity[0][0]
        error_message_2 = f'주문하신 메뉴의 수량이 부족합니다. (잔여 수량: {quantity_data})'
        return error_message_2

@app.route('/result')
def result():
    cursor.execute("SELECT * FROM menus_v2")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
