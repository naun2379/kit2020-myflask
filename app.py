from flask import Flask, request ,redirect, render_template, url_for , abort, session
app = Flask(__name__)

import game
import json
import random
import dbdb

app.secret_key = b'aaa!111/'

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/hello')
def hello():
    return 'Hello,World'

@app.route('/hello/<name>')
def hellovar(name):
    character = game.set_charact(name)
    return render_template('gamestart.html', data=character)

@app.route('/gamestar')
def gamestar():
    return render_template('gamestar.html')


w=["cat","dog","fow","monkey","mouse","panda","banana","apple","frog",]
count = {}
quest = {}

@app.route('/gamestart', methods=['GET','POST'])
def gamestart():
    if request.method == 'GET':
        count[session["user"]] = 0
        quest[session["user"]] = random.choice(w)
        return render_template('gamestart.html', quest=quest[session["user"]])
    else:
        answer = request.form['answer']
        if answer == quest[session["user"]]:
            count[session["user"]] += 1
            if count[session["user"]] >=5: #밑에게임승리소스
                return '''  
                    <script> alert('오타가없으시네요 메인으로 돌아갑니다');
                    location.href="/"
                    </script> 
                    '''

            else:
                quest[session["user"]] = random.choice(w)
                return render_template('gamestart.html', quest=quest[session["user"]])
        else:
            return '''
                    <script> alert('오타입니다!!!!처음부터 다시시작하세요!');
                    location.href="/gamestar"
                    </script>
                    '''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        ret = dbdb.select_user(id, pw)
        if ret != None:
            session['user'] = id
            return '''
                <script> alert('안녕하세요~ {}님');
                location.href="/"
                </script>
                '''.format(ret[2])
        else:
            return '''
                <script> alert('아이디 또는 패스워드를 확인 하세요');
                location.href="/login"
                </script>
                '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form["id"]
        pw = request.form["pw"]
        name = request.form["name"]
        if id == "":
            return '''
                <script>
                alert('아이디를 입력 해주세요');
                location.href='/join';
                </script>
                '''
        elif pw == "":
            return '''
                <script>
                alert('비밀번호를 입력 해주세요');
                location.href='/join';
                </script>
                '''
        elif name == "":
            return '''
                <script>
                alert('이름을 입력 해주세요');
                location.href='/join';
                </script>
                '''
        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                <script>
                alert('다른 아이디를 사용하세요');
                location.href='/join';
                </script>
                '''
        # id와 pw가 db 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
        dbdb.insert_user(id, pw, name)
        return redirect(url_for('login'))


@app.route('/form')
def form():
    return render_template('test.html')

@app.route('/method',methods=['get','post'])
def method():
    if request.method == 'Get':
        return 'get 으로 전송이다.'
    else:
        num = request.form['num']
        name = request.form['name']
        print(num , name)
        dbdb.insert_data(num,name)
        return 'post이다. 학번은:{} 이름은:{}'. format(num , name)

@app.route('/getinfo')
def getinfo():
    if 'user' in session:
        ret = dbdb.select_all()
        return render_template('getinfo.html', data=ret)
    return '''
        <script> alert('로그인 후에 이용 가능합니다');
        location.href="/login"
        </script>
        '''

@app.route('/naver')
def naver():
    return redirect("https://www.naver.com/")
    # return render_template("naver.html")

@app.route('/kakao')
def daum():
    return redirect("https://www.daum.net/")

@app.route('/urltest')
def url_test():
    return redirect(url_for('naver'))

@app.route('/move/<site>')
def move_site(site):
    if site == 'naver':
        return redirect(url_for('naver'))
    elif site == 'daum':
        return redirect(url_for('daum'))
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return "페이지가 없습니다. url을 확인하세요  ",404

@app.route('/img')
def img():
    return render_template('image.html')

if __name__ == '__main__':
    #with app.test_request_context():
       # print(url_for('daum'))
    app.run(debug=True)
