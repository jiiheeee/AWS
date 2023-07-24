from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'DB_TEST2'

mysql=pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    autocommit=True
)

cursor=mysql.cursor()

#메인화면
@app.route('/', methods =['GET'])
def main():
    return render_template('main.html')

#게시글 목록
@app.route('/board_list', methods=['POST'])
def board_list():
    cursor.execute("SELECT * FROM board")
    data = cursor.fetchall()
    return render_template('board_list.html', data=data)

#게시글 글쓰기
@app.route('/board_posting', methods=['POST'])
def board_posting():
    return render_template('board_posting.html')

#작성하기 누른 후 DB 저장 및 목록 보여주기
@app.route('/result', methods=['POST'])
def result():
    id=request.form['id']
    title=request.form['title']
    content=request.form['content']
    cursor.execute(f"insert into board (id, title, content) values ('{id}', '{title}', '{content}')")
    
    cursor.execute("select * from board")
    data = cursor.fetchall()
    return render_template('board_list.html', data=data)

# 파란 링크 누르면 이동
@app.route('/board_list/<number>')
def show_post(number):
    cursor.execute(f"SELECT * FROM board WHERE number = '{number}'")
    post = cursor.fetchone()


    return render_template('board_detail.html', post=post)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)