"""
Budget management routes for the application.
Handles CRUD operations for budget entries and budget statistics.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.budget import Budget
from app.forms import BudgetForm
from datetime import datetime

budgets = Blueprint('budgets', __name__)

@budgets.route('/budgets')
@login_required
def index():
    """
    Displays the list of budget entries and total statistics.
    """
    budgets = Budget.select().order_by(Budget.date.desc())
    total_expenses = sum(b.amount for b in budgets if b.is_expense)
    total_income = sum(b.amount for b in budgets if not b.is_expense)
    return render_template('budgets/list.html', budgets=budgets, total_expenses=total_expenses, total_income=total_income)

@budgets.route('/budgets/new', methods=['GET', 'POST'])
@login_required
def new():
    """
    Creates a new budget entry.
    """
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
        return redirect(url_for('budgets.index'))
    return render_template('budgets/form.html', form=form, title='Ajouter un budget')

@budgets.route('/budgets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edits an existing budget entry.
    """
    budget = Budget.get_or_none(Budget.id == id)
    if not budget:
        flash('Budget non trouvé', 'error')
        return redirect(url_for('budgets.index'))
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
        return redirect(url_for('budgets.index'))
    return render_template('budgets/form.html', form=form, title='Modifier le budget')

@budgets.route('/budgets/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """
    Deletes a budget entry.
    """
    budget = Budget.get_or_none(Budget.id == id)
    if not budget:
        flash('Budget non trouvé', 'error')
        return redirect(url_for('budgets.index'))
    budget.delete_instance()
    flash('Budget supprimé avec succès', 'success')
    return redirect(url_for('budgets.index'))

@budgets.route('/budgets/statistics')
@login_required
def statistics():
    """
    Displays budget statistics including monthly totals and category breakdown.
    """
    # Get all budgets
    budgets = Budget.select()
    
    # Calculate monthly totals
    monthly_expenses = {}
    monthly_income = {}
    
    for budget in budgets:
        month = budget.date.strftime('%Y-%m')
        if budget.is_expense:
            monthly_expenses[month] = monthly_expenses.get(month, 0) + budget.amount
        else:
            monthly_income[month] = monthly_income.get(month, 0) + budget.amount
    
    # Calculate category totals
    category_expenses = {}
    category_income = {}
    
    for budget in budgets:
        category = budget.description.split()[0] if budget.description else 'Other'
        if budget.is_expense:
            category_expenses[category] = category_expenses.get(category, 0) + budget.amount
        else:
            category_income[category] = category_income.get(category, 0) + budget.amount
    
    return render_template('budgets/statistics.html',
                         monthly_expenses=monthly_expenses,
                         monthly_income=monthly_income,
                         category_expenses=category_expenses,
                         category_income=category_income) 