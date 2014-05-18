from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os

app = Flask(__name__)
# encryption key for CSRF protection
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)

# database-related configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# With an ORM, the model (a Python class) is mapped to
# columns in a corresponding database table

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text(100))
    directions = db.Column(db.Text(1000))
    # one-to-many relationship from tags to recipes
    # TODO -- should be many-to-many
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    
    def __repr__(self):
        return 'Recipe %r' % self.name


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    quantity = db.Column(db.String(64))
    # TODO -- one-to-one relationship between Ingredients and Recipes
    
    def __repr__(self):
        return 'Ingredient %r' % self.name


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # one-to-many relationship from tags to recipes
    # TODO -- should be many-to-many
    recipes = db.relationship('Recipe', backref='tag')
    
    def __repr__(self):
        return 'Tag %r' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe.query.filter_by(name=form.name.data).first()
        if recipe is None:
            recipe = Recipe(name=form.name.data)
            db.session.add(recipe)
            flash('Adding new recipe!')
        else:
            flash('That recipe has already been added')
        session['rname'] = form.name.data
        form.name.data = ''
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

