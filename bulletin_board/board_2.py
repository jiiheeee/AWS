from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # 사용자로부터 전송된 데이터를 받아옵니다.
        title = request.form['title']
        content = request.form['content']

        # 받아온 데이터를 처리하거나 저장하는 코드를 추가할 수 있습니다.
        # 여기서는 간단히 출력만 하겠습니다.
        print(f"Title: {title}, Content: {content}")

    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
