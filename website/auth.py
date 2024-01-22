# website/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Post, Comment, Like
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Define the 'auth' Blueprint
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Handle user login
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            # Check if the entered password is correct
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    # Render the login page
    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Handle user registration
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # Check for various registration validation conditions
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            # Create a new user and add them to the database
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    # Render the signup page
    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    # Log out the user
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/user-settings", methods=['GET', 'POST'])
@login_required
def user_settings():
    # Handle user settings updates
    if request.method == 'POST':
        new_password = request.form.get("new_password")
        new_username = request.form.get("new_username")

        # Update password
        if new_password:
            current_user.password = generate_password_hash(new_password, method='sha256')

        # Update username
        if new_username:
            current_user.username = new_username

        # Commit changes to the database
        db.session.commit()

        flash('User settings updated!', category='success')

    # Render the user settings page
    return render_template("user_settings.html", user=current_user)

@auth.route("/user-settings/update-password", methods=['POST'])
@login_required
def update_password():
    # Handle updating the user's password
    new_password = request.form.get("new_password")

    if new_password:
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Password updated!', category='success')
    else:
        flash('Please provide a new password.', category='error')

    return redirect(url_for('auth.user_settings'))


@auth.route("/user-settings/update-username", methods=['POST'])
@login_required
def update_username():
    # Handle updating the user's username
    new_username = request.form.get("new_username")

    if new_username:
        current_user.username = new_username
        db.session.commit()
        flash('Username updated!', category='success')
    else:
        flash('Please provide a new username.', category='error')

    return redirect(url_for('auth.user_settings'))

@auth.route("/user-settings/delete-account", methods=['POST'])
@login_required
def delete_account():
    # Delete associated comments and likes before deleting the user account
    Comment.query.filter_by(author_id=current_user.id).delete()
    Like.query.filter_by(author_id=current_user.id).delete()

    # Delete the user account
    db.session.delete(current_user)
    db.session.commit()

    # Log out the user after deleting the account
    logout_user()

    flash('Your account has been deleted.', category='success')
    return redirect(url_for('views.home'))