"""
Budget model for the application.
Represents budget entries for expenses and income using Peewee ORM.
"""

from app.models.bdd import db
from peewee import *
from datetime import datetime

class Budget(db.Model):
    """
    Model representing a budget entry (expense or income).
    Stores name, category, amount, description, date, and type (expense/income).
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)  # Budget name
    category = CharField(max_length=50, null=False)  # e.g., food, vet, accessories
    amount = FloatField(null=False)
    description = TextField(null=True)
    date = DateField(null=False)
    is_expense = BooleanField(default=True)  # True for expense, False for income
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'budgets'

    def save(self, *args, **kwargs):
        """
        Updates the 'updated_at' timestamp on every save.
        """
        self.updated_at = datetime.now()
        return super(Budget, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category} - {self.amount}€ ({self.date})"

    def to_dict(self):
        """
        Returns a dictionary representation of the budget entry.
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'is_expense': self.is_expense,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }