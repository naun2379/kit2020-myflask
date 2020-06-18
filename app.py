from flask import Flask, request ,redirect, render_template, url_for , abort, session
app = Flask(__name__)

import game
import json

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

@app.route('/gamestart')
def gamestart():
    with open("static/save.txt","r",encoding='utf-8') as f:
        data = f.read()
        character = json.loads(data)
        print(character['items'])
    return "{}이 {}아이템을 사용해서 이겼습니다.".format(character["name"],character["items"][0])

#@app.route('/input/<int:num>')
#def input_num(num):
    #if num == 1:
        #with open("static/save.txt","r",encoding='utf-8') as f:
            #data = f.read()
            #character = json.loads(data)
            #print(character['items'])
    #return "{}이 {}아이템을 사용해서 이겼습니다.".format(character["name"],character["items"][0])
    #elif num == 2:
        #return "도망갔다"
    #elif num == 3:
        #return "퉁퉁이"
    #else:
        #return "없어요"
    #return 'hello, {}!' . format(name)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        print (id,type(id))
        print (pw,type(pw))
        ret = dbdb.select_user(id,pw)
        print(ret[2])
        if ret != None:
            session['user'] = id
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/join', methods=['GET','POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        print (id,type(id))
        print (pw,type(pw))
        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                    <Script>
                    alert('다른아이디를 사용하세요');
                    location.href='/join';
                    <script>
                '''
        dbdb.insert_user(id,pw,name)
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
        print(ret[3])
        return render_template('getinfo.html',date=ret)

    return redirect(url_for('login'))
    #return '번호 : {},이름 : {}',format(student[0],student[1])

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

#if __name__ == '__main__':
    #with app.test_request_context():
       # print(url_for('daum'))
    #app.run(debug=True)