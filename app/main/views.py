from flask import render_template, session, redirect, \
    url_for, flash, current_app
from . import main
from .forms import RecipeForm
from .. import db
from ..models import Recipe
from ..email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe.query.filter_by(name=form.name.data).first()
        if recipe is None:
            recipe = Recipe(name=form.name.data)
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
