from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap4
from flask_moment import Moment
import pytz

app = Flask(__name__)
bootstrap = Bootstrap4(app)
moment = Moment(app)


@app.route("/")
def index():
    # return "<h1>Hello World</h1>"
    current_time = datetime.utcnow()
    return render_template("index.html", current_time=current_time)


@app.route("/user/<name>")
def user(name):
    # return "<h1>Hello, {}!<3</h1>".format(name)
    page = request.args.get('page')
    number = request.args.get('number')
    print("Page is: ", page, " - Number is: ", number)
    return render_template("user.html", name=name, page=page, number=number)


@app.route('/get-date-time/<string:region_code>/<string:city_code>')
def getdate(region_code, city_code):
    # current_time = datetime.utcnow()
    # print(current_time)
    time_string = region_code.title() + "/" +city_code.title()
    if time_string in pytz.all_timezones:
        current_time = datetime.now(pytz.timezone(time_string))
        print(True)
    else:
        current_time = datetime.utcnow()
        print(False)
    return render_template('ex4.html', number=4, current_time=current_time)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(505)
def internal_server_error(e):
    return render_template("505.html"), 505
