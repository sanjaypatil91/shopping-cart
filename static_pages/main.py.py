from flask import Flask

app=Flask(__name__)

app@route('/static_pages/<path:file_name>')


@app.route('/static_pages/<path:file_path>')
def send_static_pages(file_path):
    return send_from_directory("static_pages", file_path)


   
if __name__=="__main__":
    app.run(host="0.0.0.0", port=50000)
