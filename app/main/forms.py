from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms import TextAreaField
from wtforms.validators import Required, NumberRange


class RecipeForm(Form):
    name = StringField('Name:', validators=[Required()])
    description = StringField('Description:')
    directions = TextAreaField('Directions:', validators=[Required()])
    ingredients = TextAreaField('Ingredients:', validators=[Required()])
    prep_time = StringField('Preparation Time:')
    num_portions = IntegerField('Number of Portions:',
                                validators=[NumberRange(1, 12)])
    source = StringField('Source:')
    image = FileField('Image:')
    tags = StringField('Tags:')
    submit = SubmitField('Submit')
