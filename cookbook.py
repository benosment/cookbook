from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.route('/recipe/<name>')
def recipe(name):
    return '<h1>Showing recipe: %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)

