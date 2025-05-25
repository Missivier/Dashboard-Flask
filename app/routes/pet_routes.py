from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.pet import Pet
from app.forms import PetForm

bp = Blueprint('pets', __name__)

@bp.route('/pets')
@login_required
def list_pets():
    pets = Pet.select().where(Pet.owner == current_user)
    return render_template('pets/list.html', pets=pets)

@bp.route('/pets/new', methods=['GET', 'POST'])
@login_required
def create_pet():
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
        flash('Animal ajouté avec succès !', 'success')
        return redirect(url_for('pets.list_pets'))
    return render_template('pets/form.html', form=form, title='Ajouter un animal')

@bp.route('/pets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pet(id):
    try:
        pet = Pet.get((Pet.id == id) & (Pet.owner == current_user))
    except Pet.DoesNotExist:
        flash('Animal non trouvé ou vous n\'avez pas l\'autorisation de le modifier.', 'error')
        return redirect(url_for('pets.list_pets'))
    
    form = PetForm(obj=pet)
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.breed = form.breed.data
        pet.birth_date = form.birth_date.data
        pet.weight = form.weight.data
        pet.save()
        flash('Animal modifié avec succès !', 'success')
        return redirect(url_for('pets.list_pets'))
    return render_template('pets/form.html', form=form, title='Modifier un animal')

@bp.route('/pets/<int:id>/delete', methods=['POST'])
@login_required
def delete_pet(id):
    try:
        pet = Pet.get((Pet.id == id) & (Pet.owner == current_user))
        pet.delete_instance()
        flash('Animal supprimé avec succès !', 'success')
    except Pet.DoesNotExist:
        flash('Animal non trouvé ou vous n\'avez pas l\'autorisation de le supprimer.', 'error')
    return redirect(url_for('pets.list_pets')) 