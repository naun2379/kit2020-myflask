import sqlite3
conn = sqlite3.connect('mydb.db')
# Cursor 객체 생성
c = conn.cursor()

# 학번을 검색해서 정보 출력
num = ('20171070',)
c.execute('SELECT * FROM student WHERE num = ? ',num)
print(c.fetchone())

# 접속한 db 닫기
conn.close()