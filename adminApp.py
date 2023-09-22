from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'Student'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('student-signup.html')




@app.route("/addstudent", methods=['GET', 'POST'])
def AddStu():
    student_email = request.form['student_email']
    student_password = request.form['student_password']


    insert_sql = "INSERT INTO Student VALUES (%s, %s)"
    cursor = db_conn.cursor()


    try:

        cursor.execute(insert_sql, (student_email, student_password))
        db_conn.commit()
       

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('login.html')

@app.route("/studentlogin", methods=['GET', 'POST'])
def StudentLogin():
    
    student_email = request.form['student_email']
    student_password = request.form['student_password']
        
    select_sql = "SELECT * FROM Student WHERE student_email = %s AND student_password = %s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (student_email, student_password))
        student = cursor.fetchone()

        if student:

                
            return render_template('home.html')  # You can redirect to a dashboard or student page
        else:
            return render_template('login.html')

    except Exception as e:
        print(f"Error: {e}")
    finally:
            cursor.close()

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

