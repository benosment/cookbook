from flask import render_template, session, redirect, \
    url_for, flash, current_app
from . import main
from .forms import RecipeForm
from .. import db
from ..models import Recipe
from ..email import send_email
from datetime import datetime

# TODO
# - change index to show a list of all recipes
## @app.route('/')
## def show_recipes():
##   recipes = Recipe.query.all()
##   return render_template('show_recipes.html', recipes=recipes)
# 
# - move old index to add
# - add a link for add on main page
# - add all fields in the recipe into the form
#  - in the form, have a diag file selector for the field
# - lowercase the title of recipe
# - create an edit page
## def edit_profile(request):
##    user = User.objects.get(pk=request.session['userid'])
##    form = EditProfileForm(request.POST, obj=user)
##
##    if request.POST and form.validate():
##        form.populate_obj(user)
##        user.save()
##        return redirect('/home')
##    return render_to_response('edit_profile.html', form=form)
# - create a script which backups the database periodically
@main.route('/', methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe.query.filter_by(name=form.name.data).first()
        if recipe is None:
            recipe = Recipe(name=form.name.data,
                            description=form.description.data,
                            directions=form.directions.data,
                            ingredients=form.ingredients.data,
                            preparation_time=form.prep_time.data,
                            num_portions=form.num_portions.data,
                            source=form.source.data,
                            date_created=datetime.utcnow(),
                            date_updated=datetime.utcnow(),
                            img_location=form.image.data,
                            tags=form.tags.data)
            db.session.add(recipe)
            flash('Adding new recipe!')
            if current_app.config['COOKBOOK_ADMIN']:
                send_email(current_app.config['COOKBOOK_ADMIN'],
                           'New recipe', 'mail/new_recipe',
                           recipe=recipe)
        else:
            flash('That recipe has already been added')
        session['rname'] = form.name.data
        form.name.data = ''
        # always end POSTs with a redirect
        # this elimates issues when refreshing the page
        return redirect(url_for('.index'))
    return render_template("index.html", form=form,
                           rname=session.get('rname'))
