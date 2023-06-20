from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 7 characters.', category='error')
        else:
            newUser = Users(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)


# @auth.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     if request.method == 'POST':
#         email = request.form.get('email')
#
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             # Create a password reset token
#             reset_token = generate_password_reset_token(user.email)
#             # Send the password reset email
#             send_password_reset_email(user.email, reset_token)
#             flash('Password reset email has been sent.', category='success')
#             return redirect(url_for('auth.login'))
#         else:
#             flash('Email does not exist.', category='error')
#
#     return render_template("reset_password.html", user=current_user)
#
#
# @auth.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password_token(token):
#     if request.method == 'POST':
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#
#         user = verify_password_reset_token(token)
#         if user:
#             if password1 != password2:
#                 flash('Passwords don\'t match.', category='error')
#             elif len(password1) < 7:
#                 flash('Password must be at least 7 characters.', category='error')
#             else:
#                 # Update the user's password
#                 user.password = generate_password_hash(password1, method='sha256')
#                 db.session.commit()
#                 flash('Password has been reset.', category='success')
#                 return redirect(url_for('auth.login'))
#         else:
#             flash('Invalid or expired token.', category='error')
#
#     return render_template("reset_password_token.html", user=current_user)
#
#
# def generate_password_reset_token(email):
#     # Create a password reset token for the user
#     token = "<generate a unique password reset token>"
#     # Save the token to the database
#     password_reset_token = PasswordResetToken(email=email, token=token)
#     db.session.add(password_reset_token)
#     db.session.commit()
#     return token
#
#
# def verify_password_reset_token(token):
#     # Query the database for a password reset token
#     password_reset_token = PasswordResetToken.query.filter_by(token=token).first()
#     if password_reset_token and not password_reset_token.is_expired():
#         # Get the user associated with the token
#         user = Users.query.filter_by(email=password_reset_token.email).first()
#         return user
#     return None
#
#
# def send_password_reset_email(email, token):
#     # Create the password reset email message
#     message = Message(
#         subject='Password Reset',
#         sender='noreply@example.com',
#         recipients=[email],
#         body=f"To reset your password, click the following link: {url_for('auth.reset_password_token', token=token, _external=True)}"
#     )
#     # Send the email
#     mail.send(message)
