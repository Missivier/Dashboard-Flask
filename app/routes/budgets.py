from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.budget import Budget
from app.forms import BudgetForm
from datetime import datetime

budgets = Blueprint('budgets', __name__)

@budgets.route('/budgets')
@login_required
def list_budgets():
    budgets = Budget.select().order_by(Budget.date.desc())
    total_expenses = sum(b.amount for b in budgets if b.is_expense)
    total_income = sum(b.amount for b in budgets if not b.is_expense)
    return render_template('budgets/list.html', budgets=budgets, total_expenses=total_expenses, total_income=total_income)

@budgets.route('/budgets/new', methods=['GET', 'POST'])
@login_required
def create_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget(
            name=form.name.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            date=form.date.data,
            is_expense=form.is_expense.data
        )
        budget.save()
        flash('Budget ajouté avec succès', 'success')
        return redirect(url_for('budgets.list_budgets'))
    return render_template('budgets/form.html', form=form, title='Ajouter un budget')

@budgets.route('/budgets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_budget(id):
    budget = Budget.get_or_none(Budget.id == id)
    if not budget:
        flash('Budget non trouvé', 'error')
        return redirect(url_for('budgets.list_budgets'))
    form = BudgetForm(obj=budget)
    if form.validate_on_submit():
        budget.name = form.name.data
        budget.category = form.category.data
        budget.amount = form.amount.data
        budget.description = form.description.data
        budget.date = form.date.data
        budget.is_expense = form.is_expense.data
        budget.save()
        flash('Budget mis à jour avec succès', 'success')
        return redirect(url_for('budgets.list_budgets'))
    return render_template('budgets/form.html', form=form, title='Modifier le budget')

@budgets.route('/budgets/<int:id>/delete', methods=['POST'])
@login_required
def delete_budget(id):
    budget = Budget.get_or_none(Budget.id == id)
    if not budget:
        flash('Budget non trouvé', 'error')
        return redirect(url_for('budgets.list_budgets'))
    budget.delete_instance()
    flash('Budget supprimé avec succès', 'success')
    return redirect(url_for('budgets.list_budgets')) 