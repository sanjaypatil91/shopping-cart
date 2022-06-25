from flask import Flask, send_from_directory, render_template, redirect, url_for, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "some_random_key"

@app.route('/catlog1')
def show_catlog1():
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

    page = render_template("catlog1.html", records=result, username=username)
    return page


@app.route('/add_to_cart')
def add_to_cart():
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
    return redirect(url_for("show_catlog1"))

@app.route('/showcart')
def showcart():
    if 'username' not in session:
        return redirect(url_for("login"))
    if 'cart' not in session:
        session['cart'] = {}
    
    cart_total = 0
    all_records=[]
    for product_id,product_count in session['cart'].items():
        product = get_product_from_database(product_id)
        if len(product) != 1:
            raise Exception(f" For Product id {product_id } product count fetched from database is {len(product)}")

        a_product = product[0]
        record = list(a_product) + [product_count]
        del record[3]

        total_item= record[3] + record[4]
        record.append(total_item)
        cart_total = cart_total + total_item
        all_records.append(record)

    return render_template("show_cart.html", all_records = all_records, cart_total = cart_total, username=session['username'])


def get_product_from_database(product_id):
    query=f"""select * from product where id = '{product_id}';"""

    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
    except Exception as e:
        print(e)
        return None

    return result

@app.route('/')
def home_page():
    return redirect(url_for("show_catlog1"))


@app.route('/Ship_cart')
def Ship_cart():
    all_records = []
    cart_total = 0


    for product_id,product_count in session['cart'].items():
        product = get_product_from_database(product_id)
        a_product = product[0]
        a_product = list(a_product)
        a_product[3] = a_product[3] - product_count
        update_product_inventory_count(a_product[0], a_product[3])

    session['cart'] = {}
    session.modified = True
    return render_template("show_cart.html", all_records = all_records, cart_total = cart_total, username=session['username'])


def update_product_inventory_count(product_id, inventory_count):
    query = f""" UPDATE Product 
                 SET inventory_quantity= {inventory_count}
                 WHERE id = '{product_id}'
                 """
    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
    except Exception as e:
        print(e)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        page = render_template("login.html")
        return page
    elif request.method == "POST":
        user_id = request.form['username']
        password = request.form['password']
        all_users = getuser_from_userid(user_id)
        print(all_users)

        if len(all_users) == 0:
            page = render_template("login.html")
            return page
        elif len(all_users) > 1:
            raise Exception(f"Multiple users with same userid present")
   
        user = all_users[0]
        if user[2] == password:
            session['username'] = request.form['username']
            return redirect(url_for("show_catlog1"))
        else:
            page = render_template("login.html")
            return page


@app.route('/signup', methods =['GET', 'POST'])
def signup():
 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        page = render_template("signup.html")
        return page

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = cursor.fetchall()
        if account:
            cursor.execute(query)
            connection.commit()
            msg = 'You have successfully signed up !'
    elif request.method == 'POST':
       page=render_template('signup.html')
       return page


    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute("select * from product")
                result = cursor.fetchall()
    except Exception as e:
        print(e)



def getuser_from_userid(userid):
    query = f"""select * from user where name = '{userid}';"""

    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
    except Exception as e:
        print(e)
        return None

    return result


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for("show_catlog1"))


@app.route('/static_pages/<path:file_name>')
def static_pages(file_name):
   return send_from_directory('static_pages', file_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000)