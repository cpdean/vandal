from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from generate import generate, test_repo
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == 'POST':
        date = request.json["startDate"]
        painted = request.json["painted"]
        user_full_name = request.json.get("user_full_name", None)
        user_email = request.json.get("user_email", None)
        print date
        print pretty_canvas(painted)
        generate(test_repo(), date, painted,
                 author=user_full_name, email=user_email)
        return "OK"


@app.route('/user')
def user():
    username = request.args["username"]
    r = requests.get("https://api.github.com/users/" + username)
    print r
    name = r.json().get('name', None)
    email = r.json().get('email', None)
    return jsonify(user_full_name=name, user_email=email)


def pretty(cells):
    return "".join(["." if i == 0 else str(i) for i in cells])


def pretty_canvas(cells):
    days_of_week = []
    for day in range(7):
        days = [i for i in cells[day::7]]
        days_of_week.append(pretty(days))
    return "\n".join(days_of_week)

if __name__ == '__main__':
    app.debug = True
    app.run()
