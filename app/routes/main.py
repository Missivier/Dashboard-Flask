from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.models.user import User, Role
from app.models.house import House
from app.models.task import Task, ListTask
from app.forms import RegisterForm, LoginForm, CreateHouseForm, ProfileForm, TaskForm, ListTaskForm, TestForm
from app.models.budget import Budget
from app.models.event import Event
from app.models.pet import Pet
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    house = user.house
    # Récupérer les listes de tâches et les tâches
    lists = ListTask.select()
    tasks = Task.select().where(Task.list_task.is_null(False))
    # Récupérer tous les budgets
    budgets = Budget.select()
    total_expenses = sum(b.amount for b in budgets if b.is_expense)
    total_income = sum(b.amount for b in budgets if not b.is_expense)
    # Récupérer les animaux de l'utilisateur
    pets = Pet.select().where(Pet.owner == current_user)
    # Récupérer les événements à venir et d'aujourd'hui
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    upcoming_events = Event.select().where(
        (Event.user_id == current_user.id) &
        (Event.start_date >= tomorrow)
    ).count()
    
    today_events = Event.select().where(
        (Event.user_id == current_user.id) &
        (Event.start_date >= today) &
        (Event.start_date < tomorrow)
    ).count()
    
    return render_template('dashboard.html',
                         user=user,
                         house=house,
                         lists=lists,
                         tasks=tasks,
                         budgets=budgets,
                         pets=pets,
                         total_expenses=total_expenses,
                         total_income=total_income,
                         upcoming_events=upcoming_events,
                         today_events=today_events)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name_user = form.name_user.data
        current_user.first_name_user = form.first_name_user.data
        current_user.username_user = form.username_user.data
        current_user.email_user = form.email_user.data
        current_user.phone_user = form.phone_user.data
        current_user.age_user = form.age_user.data
        current_user.date_birthday_user = form.date_birthday_user.data
        current_user.description_user = form.description_user.data
        current_user.save()
        flash('Profil mis à jour avec succès !', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form)

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

@main.route('/test-csrf', methods=['GET', 'POST'])
def test_csrf():
    form = TestForm()
    if form.validate_on_submit():
        return jsonify({
            'success': True,
            'message': 'Formulaire soumis avec succès',
            'data': form.message.data
        })
    return render_template('test_csrf.html', form=form)

@main.route('/test-csrf-api', methods=['POST'])
def test_csrf_api():
    if not request.is_json:
        return jsonify({'error': 'Content-Type doit être application/json'}), 400
    
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'Requête API traitée avec succès',
        'data': data
    }) 