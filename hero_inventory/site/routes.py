from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from hero_inventory.forms import HeroForm
from hero_inventory.models import Hero, db
from hero_inventory.helpers import random_marvel_genorator



site = Blueprint('site', __name__ , template_folder='site_templates')


@site.route('/')
def home():
    print('this is inside of site routes')
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_hero = HeroForm() #data coming back from my hero

    try:
        print('here I am at the try')
        if request.method == "POST" and my_hero.validate_on_submit():
            name = my_hero.name.data
            description = my_hero.description.data
            comic_in = my_hero.comic_in.data
            super_power = my_hero.super_power.data
            if my_hero.random_quote.data:
                random_quote = my_hero.random_quote.data
            else:
                random_quote = random_marvel_genorator()
            user_token = current_user.token

            hero = Hero(name, description, comic_in, super_power, random_quote, user_token)

            db.session.add(hero)
            db.session.commit()
            print('Should be in the data base')
            return redirect(url_for('site.profile'))

    except:
        raise Exception('Hero Not created: please check form again')
    print('missed the exception')
    current_user_token = current_user.token

    heros = Hero.query.filter_by(user_token=current_user_token)

    
    return render_template('profile.html', form=my_hero, heros = heros)
    