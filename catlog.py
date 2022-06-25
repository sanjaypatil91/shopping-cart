

from flask import Flask, send_from_directory
import mysql.connector

app = Flask(__name__)

catlog_table1="""

<html>
<head></head>
<body>

<table border="1">
    <tr>
        <th>Product ID</th>
        <th>Name</th>
        <th>Image</th>
        <th>Amount</th>
        <th>Action</th>
    </tr>

"""
catlog_table2 = ""

catlog_table3 = """
</table>

</body>

</html>


"""

@app.route('/catlog')
def show_catlog():
    global catlog_table2
    resule = []
    try:
        with mysql.connector.connect(host="localhost",user="root",password="password_123",database="shopping_cart") as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from product")
                result = cursor.fetchall()
    except Error as e:
        print(e)


    for item in result:
        product_html = f"""<tr>
            <th>{item[0]}</th>
            <th>{item[1]}</th>
            <th><img src="{item[2]}"  alt="Image" height="100" width="70"/></th>
            <th>{item[4]}</th>
            <th><b>Buy</b></th>
        </tr>"""

        catlog_table2 = catlog_table2 + product_html

    return catlog_table1 + catlog_table2 + catlog_table3

@app.route('/static_pages/<path:file_name>')
def static_pages(file_name):
   return send_from_directory('static_pages', file_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000)