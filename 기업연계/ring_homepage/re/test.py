from flask import Flask, session, render_template, redirect, request, url_for, send_from_directory
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1q2w3e4r'
app.config['MYSQL_DB'] = 'ring'
app.secret_key = 'ABCDEF'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    error = None

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        conn = mysql.connection
        cursor = conn.cursor()

        sql = "SELECT user_id FROM member WHERE user_id = '%s' AND user_passwd = '%s' " % (id, pw)

        # print(sql)
        # cursor.execute("set names utf8")
        cursor.execute(sql)

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in data:
            data = row[0]

        if data:
            session['login_id'] = id
            return redirect(url_for('home',name=id))
        else:
            error = 'invalid input data detected !'

    return render_template('index-8.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['regi_id']
        pw = request.form['regi_pw']
        pw_ck = request.form['regi_pw_chk']
        name = request.form['regi_name']
        email = request.form['regi_email']

        conn = mysql.connection
        cursor = conn.cursor()

        sql = "INSERT INTO member(user_id, user_name, user_email, user_passwd, user_pw_ck) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, name, email, pw, pw_ck)
        cursor.execute(sql)

        data = cursor.fetchall()

        if not data:
            conn.commit()
            return redirect(url_for('main'))
        else:
            conn.rollback()
            return "Register Failed"

        cursor.close()
        conn.close()

    return render_template('create_account.html', error=error)

@app.route('/home.html/<name>', methods=['GET', 'POST'])
def home(name):
    error = None
    return render_template('home.html', name=name)
    
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)