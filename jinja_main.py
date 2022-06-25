from flask import Flask, send_from_directory, render_template, redirect, url_for, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "some_random_key"

@app.route('/catlog')
def show_catlog():
    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute("select * from product")
                result = cursor.fetchall()
    except Exception as e:
        print(e)

    username = None
    if 'username' in session:
        username = session['username']
    print(session)

    page = render_template("catlog.html", records=result, username=username)
    return page


@app.route('/add_to_cart')
def addtocart():
    print(request.args)
    print(session)

    if 'username' not in session:
        return redirect(url_for("login"))

    if 'cart' not in session:
        session['cart']={}

    if request.args['product_id'] not in session['cart']:
        session['cart'][request.args['product_id']] = 0

    session['cart'][request.args['product_id']] = session['cart'][request.args['product_id']] + 1
    session.modified = True
    return redirect(url_for("show_catlog"))

@app.route('/Show_Cart')
def Show_Cart():
    return render_template("show_cart.html")



@app.route('/')
def home_page():
    return redirect(url_for("show_catlog"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        page = render_template("login.html")
        return page
    elif request.method == "POST":
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['username'] = request.form['username']
            return redirect(url_for("show_catlog"))
        else:
            page = render_template("login.html")
            return page


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for("show_catlog"))


@app.route('/static_pages/<path:file_name>')
def static_pages(file_name):
   return send_from_directory('static_pages', file_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000)