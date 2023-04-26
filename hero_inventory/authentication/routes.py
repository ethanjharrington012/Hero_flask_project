from flask import Blueprint, render_template, request, redirect, url_for, flash
from hero_inventory.forms import UserLoginForm
from hero_inventory.models import User, db
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            print(email, username, password)

            user = User(email, username, password=password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have created a user acount {username}, user-created")

            return redirect(url_for('auth.signin'))
        
    except:
        raise Exception('Invalid Form Data: Please change your form')

    return render_template('sign_up.html',form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)


            logged_user = User.query.filter(User.email == email).first()
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):
                print(f"this is the logged user {logged_user}")
                login_user(logged_user)
                flash(f"You were successfuly logged in Via: email/password", 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash("Your email/password is incurect", 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form!')

    return render_template('/sign_in.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
