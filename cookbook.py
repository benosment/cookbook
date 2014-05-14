from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recipe/<rname>')
def recipe(rname):
    return render_template("recipe.html", recipe=rname)


if __name__ == '__main__':
    manager.run()

