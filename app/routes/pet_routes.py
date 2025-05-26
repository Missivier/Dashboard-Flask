"""
Pet management routes for the application.
Handles CRUD operations for pets and their care schedules.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.pet import Pet
from app.forms import PetForm
from datetime import datetime

bp = Blueprint('pets', __name__)

@bp.route('/pets')
@login_required
def index():
    """
    Displays the list of user's pets.
    """
    pets = Pet.select().where(Pet.owner == current_user)
    return render_template('pets/index.html', pets=pets)

@bp.route('/pets/new', methods=['GET', 'POST'])
@login_required
def new():
    """
    Creates a new pet profile.
    """
    form = PetForm()
    if form.validate_on_submit():
        pet = Pet.create(
            name=form.name.data,
            species=form.species.data,
            breed=form.breed.data,
            birth_date=form.birth_date.data,
            weight=form.weight.data,
            owner=current_user
        )
        flash('Animal ajouté avec succès', 'success')
        return redirect(url_for('pets.index'))
    
    return render_template('pets/form.html', form=form, title='Nouvel animal')

@bp.route('/pets/<int:id_pet>/edit', methods=['GET', 'POST'])
@login_required
def edit(id_pet):
    """
    Edits an existing pet profile.
    """
    pet = Pet.get_or_none(Pet.id_pet == id_pet)
    if not pet or pet.owner != current_user:
        flash('Animal non trouvé', 'error')
        return redirect(url_for('pets.index'))
    
    form = PetForm(obj=pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.breed = form.breed.data
        pet.birth_date = form.birth_date.data
        pet.weight = form.weight.data
        pet.save()
        flash('Animal modifié avec succès', 'success')
        return redirect(url_for('pets.index'))
    
    return render_template('pets/form.html', form=form, title='Modifier l\'animal')

@bp.route('/pets/<int:id_pet>/delete', methods=['POST'])
@login_required
def delete(id_pet):
    """
    Deletes a pet profile.
    """
    pet = Pet.get_or_none(Pet.id_pet == id_pet)
    if pet and pet.owner == current_user:
        pet.delete_instance()
        flash('Animal supprimé avec succès', 'success')
    else:
        flash('Animal non trouvé', 'error')
    return redirect(url_for('pets.index'))

@bp.route('/pets/<int:id_pet>/care')
@login_required
def care_schedule(id_pet):
    """
    Displays the care schedule for a specific pet.
    """
    pet = Pet.get_or_none(Pet.id_pet == id_pet)
    if not pet or pet.owner != current_user:
        flash('Animal non trouvé', 'error')
        return redirect(url_for('pets.index'))
    
    # Get upcoming care tasks
    upcoming_care = pet.get_upcoming_care()
    
    return render_template('pets/care_schedule.html',
                         pet=pet,
                         upcoming_care=upcoming_care) 