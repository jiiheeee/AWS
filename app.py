from flask import Flask, render_template, request, redirect, jsonify
import pymysql
import cryptography

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

    #! 1. `menu`와 `q`를 받아서 INSERT 쿼리문을 작성한다.
    #! 2. where문으로 menus_v2의 name이 변수 `menu`에 담긴것과 같은것들의 quantity를 변수 `q`만큼 감소시키는 UPDATE 쿼리문을 작성한다
    #! 3. routing을 하나 더 만들어서 메뉴판을 보여주는 routing을 보여준다 

@app.route('/')
def order():
    return render_template('order.html')

@app.route('/order/jihee', methods = ['POST'])
def order_jihee():
    menu = request.form['menu']
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
    cursor.execute(f"SELECT * FROM menus_v2 where name='{menu}';")

    res = cursor.fetchall()
    after_quantity = int(res[0][3]) - int(quantity)

    if int(quantity) < 0:
        error_message_1 = '수량은 1개 이상 주문해주세요.'
        return error_message_1
    
    elif int(after_quantity) >= 0:
        cursor.execute(f"UPDATE menus_v2 SET quantity = {after_quantity} WHERE name = '{menu}';")
        mysql.commit()
        return redirect('/result')

    else:
        cursor.execute(f"select quantity from menus_v2 where name = '{menu}';")
        residual_quantity = cursor.fetchall()
        quantity_data = int(residual_quantity[0][0])
        error_message_2 = f'주문하신 메뉴의 수량이 부족합니다. (잔여 수량: {quantity_data})'
        return error_message_2

@app.route('/result')
def result():
    cursor.execute("SELECT * FROM menus_v2")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
