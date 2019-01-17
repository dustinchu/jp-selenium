from flask import Flask
import getUrbanProData as gd
import os

from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler




app = Flask(__name__)  # 實例化flask


@app.route("/")
def hello():
    #return "Hello World!"
    return gd.get()




if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0",port=5000)
    #app.run("--host=127.0.0.1 --port=1234")