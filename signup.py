
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "some_random_key"



@app.route('/signup', methods =['GET', 'POST'])
def signup():
 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        page = render_template("login.html")
        return page

        userid =request.form ['userid']
        username = request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']

        account = cursor.fetchall()
        if account:
            cursor.execute(query)
            connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
       page=render_template('signup.html')
       return page


    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="register") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute("select * from user")
                result = cursor.fetchall()
    except Exception as e:
        print(e)



