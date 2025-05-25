from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.user import User, Role
from app.models.house import House
from app.forms import CreateHouseForm, ProfileForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name_user = form.name_user.data
        current_user.first_name_user = form.first_name_user.data
        current_user.username_user = form.username_user.data
        current_user.phone_user = form.phone_user.data
        current_user.age_user = form.age_user.data
        current_user.date_birthday_user = form.date_birthday_user.data
        current_user.email_user = form.email_user.data
        current_user.description_user = form.description_user.data
        current_user.save()
        flash('Profil mis à jour avec succès', 'success')
    return render_template('profile.html', user=current_user, form=form)

@main.route('/create-house', methods=['GET', 'POST'])
def create_house():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = CreateHouseForm()
    if form.validate_on_submit():
        name_house = form.name_house.data
        adress = form.adress.data
        description_house = form.description_house.data
        photo_house = form.photo_house.data
        house = House.create(
            name_house=name_house,
            adress=adress,
            description_house=description_house,
            photo_house=photo_house
        )
        current_user.house = house
        current_user.is_admin_house = True
        role_admin = Role.get_or_none(Role.name_role == 'ADMIN')
        if role_admin:
            current_user.role = role_admin
        current_user.save()
        flash('Maison créée et associée avec succès', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('create_house.html', form=form) 