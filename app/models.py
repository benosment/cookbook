from . import db

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
