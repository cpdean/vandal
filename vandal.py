from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submit', methods=["GET", "POST"])
def submit():
    if request.method == 'POST':
        print request.json["startDate"]
        print pretty_canvas(request.json["painted"])

        return "OK"


def pretty(cells):
    return "".join(["." if i == 0 else "#" for i in cells])


def pretty_canvas(cells):
    sundays = [i for i in cells[::7]]
    return pretty(sundays)

if __name__ == '__main__':
    app.debug = True
    app.run()
