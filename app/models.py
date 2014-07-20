from . import db
from datetime import datetime


# With an ORM, the model (a Python class) is mapped to
# columns in a corresponding database table
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text(100))
    directions = db.Column(db.Text(1000))
    ingredients = db.Column(db.Text(1000))
    preparation_time = db.Column(db.String(20))
    num_portions = db.Column(db.String(20))
    source = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())
    img_location = db.Column(db.String(120))
    # TODO -- should be another table, but keeping as string for
    # simplicity for now
    tags = db.Column(db.String(120))
    #tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

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
