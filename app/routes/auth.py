from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, Role
from app.forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.get_or_none(User.email_user == email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Vérification maison et rôle
            if not user.house:
                role = Role.get_or_none(Role.name_role == 'NO_HOUSE')
                if role:
                    user.role = role
                    user.save()
                return redirect(url_for('main.create_house'))
            return redirect(url_for('main.index'))
        
        flash('Email ou mot de passe incorrect', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        first_name = form.first_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = Role.get_or_none(Role.name_role == 'NO_HOUSE')
        user = User.create(
            name_user=name,
            first_name_user=first_name,
            username_user=username,
            email_user=email,
            password=generate_password_hash(password),
            role=role
        )
        
        login_user(user)
        return redirect(url_for('main.create_house'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 



