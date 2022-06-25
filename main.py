from flask import Flask, send_from_directory
import mysql.connector

app= Flask(__name__)

catlog_table="""

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

    <tr>

        <th>1</th>
        <th>Samsun phone</th>
        <th><img src="static_pages/mobile.jpg"/></th>
        <th>25000</th>
        <th><b>Buy</b></th>
    </tr>


</table>
</body>
</html>

"""

@app.route('/catlog')
def show_catlog():


    return catlog_table


@app.route('/static_pages/<path:file_name>')
def static_pages(file_name):
   return send_from_directory('static_pages', file_name)


 
if __name__=="__main__":
    app.run(host="0.0.0.0", port=50000)
    