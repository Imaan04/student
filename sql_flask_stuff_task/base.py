from flask import Flask, render_template, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec',methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']

            with sqlite3.connect("students.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city) VALUES (?,?,?)"
                            ,(name,addr,city) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html", msg=msg)

@app.route('/liststudentsL')
def listStudentsL():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from students WHERE city = 'London';")

    rows = cur.fetchall()
    return render_template("liststudentsL.html", rows=rows)

@app.route('/liststudentsS')
def listStudentsS():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from students WHERE city = 'Solihull';")

    rows = cur.fetchall()
    return render_template("liststudentsS.html", rows=rows)

@app.route('/liststudentsB')
def listStudentsB():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students WHERE city = 'Birmingham';")

    rows = cur.fetchall()
    return render_template("liststudentsB.html", rows=rows)

@app.route('/liststudents')
def listStudents():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("studentlist.html", rows=rows)

@app.route("/complete",methods=['POST', 'GET'])
def studentdeleted():
    if request.method == 'POST':
        try:
            name = request.form['name']
            print(name)

            with sqlite3.connect("students.db") as con:

                cur = con.cursor()
                cur.execute("DELETE FROM students WHERE name = ?;",(name,))
                con.commit()
                msg = "Record successfully deleted"

        except:
            con.rollback()
            msg = "error in deletion"


        finally:
            return delStudents()

@app.route('/delstudent')
def delStudents():
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row


    cur = con.cursor()
    cur.execute("select * from students")


    rows = cur.fetchall()
    con.commit()
    return render_template("delstudents.html", rows=rows)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)