from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.task import Task, ListTask, Status
from app.forms import TaskForm, ListTaskForm

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
@login_required
def index():
    """Affiche la liste des tâches"""
    tasks = Task.select().where(Task.list_task.is_null(False))
    lists = ListTask.select()
    return render_template('tasks/index.html', tasks=tasks, lists=lists)

@tasks.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new():
    """Crée une nouvelle tâche"""
    form = TaskForm()
    # Remplir les choix des select
    form.status.choices = [(s.id_status, s.name_status) for s in Status.select()]
    form.list_task.choices = [(l.id_list_task, l.name_list_task) for l in ListTask.select()]
    
    if form.validate_on_submit():
        task = Task.create(
            name_task=form.name_task.data,
            description_task=form.description_task.data,
            status=Status.get_by_id(form.status.data),
            list_task=ListTask.get_by_id(form.list_task.data)
        )
        flash('Tâche créée avec succès', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/form.html', form=form, title='Nouvelle tâche')

@tasks.route('/tasks/<int:id_task>/edit', methods=['GET', 'POST'])
@login_required
def edit(id_task):
    """Modifie une tâche existante"""
    task = Task.get_or_none(Task.id_task == id_task)
    if not task:
        flash('Tâche non trouvée', 'error')
        return redirect(url_for('tasks.index'))
    
    form = TaskForm(obj=task)
    form.status.choices = [(s.id_status, s.name_status) for s in Status.select()]
    form.list_task.choices = [(l.id_list_task, l.name_list_task) for l in ListTask.select()]
    
    if form.validate_on_submit():
        task.name_task = form.name_task.data
        task.description_task = form.description_task.data
        task.status = Status.get_by_id(form.status.data)
        task.list_task = ListTask.get_by_id(form.list_task.data)
        task.save()
        flash('Tâche modifiée avec succès', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/form.html', form=form, title='Modifier la tâche')

@tasks.route('/tasks/<int:id_task>/delete', methods=['POST'])
@login_required
def delete(id_task):
    """Supprime une tâche"""
    task = Task.get_or_none(Task.id_task == id_task)
    if task:
        task.delete_instance()
        flash('Tâche supprimée avec succès', 'success')
    else:
        flash('Tâche non trouvée', 'error')
    return redirect(url_for('tasks.index'))

@tasks.route('/tasks/lists/new', methods=['GET', 'POST'])
@login_required
def new_list():
    """Crée une nouvelle liste de tâches"""
    form = ListTaskForm()
    if form.validate_on_submit():
        list_task = ListTask.create(
            name_list_task=form.name_list_task.data
        )
        flash('Liste créée avec succès', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/list_form.html', form=form, title='Nouvelle liste')

@tasks.route('/tasks/lists/<int:id_list_task>/edit', methods=['GET', 'POST'])
@login_required
def edit_list(id_list_task):
    """Modifie une liste de tâches existante"""
    list_task = ListTask.get_or_none(ListTask.id_list_task == id_list_task)
    if not list_task:
        flash('Liste non trouvée', 'error')
        return redirect(url_for('tasks.index'))
    
    form = ListTaskForm(obj=list_task)
    if form.validate_on_submit():
        list_task.name_list_task = form.name_list_task.data
        list_task.save()
        flash('Liste modifiée avec succès', 'success')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/list_form.html', form=form, title='Modifier la liste')

@tasks.route('/tasks/lists/<int:id_list_task>/delete', methods=['POST'])
@login_required
def delete_list(id_list_task):
    """Supprime une liste de tâches"""
    list_task = ListTask.get_or_none(ListTask.id_list_task == id_list_task)
    if list_task:
        list_task.delete_instance()
        flash('Liste supprimée avec succès', 'success')
    else:
        flash('Liste non trouvée', 'error')
    return redirect(url_for('tasks.index'))

@tasks.route('/tasks/<int:id_task>/toggle', methods=['POST'])
@login_required
def toggle_status(id_task):
    """Change le statut d'une tâche (complétée/non complétée)"""
    task = Task.get_or_none(Task.id_task == id_task)
    if task:
        # Récupérer le statut "Terminé" ou le créer s'il n'existe pas
        status_completed = Status.get_or_none(Status.name_status == 'Terminé')
        if not status_completed:
            status_completed = Status.create(name_status='Terminé')
        
        # Récupérer le statut "En cours" ou le créer s'il n'existe pas
        status_in_progress = Status.get_or_none(Status.name_status == 'En cours')
        if not status_in_progress:
            status_in_progress = Status.create(name_status='En cours')
        
        # Changer le statut
        if task.is_completed:
            task.status = status_in_progress
        else:
            task.status = status_completed
        
        task.save()
        flash('Statut de la tâche mis à jour', 'success')
    else:
        flash('Tâche non trouvée', 'error')
    
    # Rediriger vers la page précédente
    return redirect(request.referrer or url_for('tasks.index')) 