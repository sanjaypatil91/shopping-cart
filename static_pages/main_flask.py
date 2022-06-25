from flask import Flask, send_from_directory
app = Flask(__name__)
import datetime

@app.route('/')
def welcome():
    return "welcome"

@app.route('/getdatetime')
def getcurrenttime():
    return str(datetime.datetime.now())


@app.route('/static_pages/<path:filename>')
def send_static_pages(filename):
    return send_from_directory("static_pages", filename)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50000)