from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
# encryption key for CSRF protection
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        session['rname'] = form.name.data
        flash('Updating database!')
        # always end POSTs with a redirect
        # this elimates issues when refreshing the page
        return redirect(url_for('index'))
    return render_template("index.html", form=form,
                           rname=session.get('rname'))

@app.route('/recipe/<rname>')
def recipe(rname):
    return render_template("recipe.html", recipe=rname)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    
class RecipeForm(Form):
    name = StringField('Recipe name:', validators=[Required()])
    submit = SubmitField('Submit')

    
if __name__ == '__main__':
    manager.run()

