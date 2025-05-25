from app.models.bdd import db
from peewee import *
from datetime import datetime

class Budget(db.Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)  # Nom du budget global
    category = CharField(max_length=50, null=False)  # ex: nourriture, vétérinaire, accessoires
    amount = FloatField(null=False)
    description = TextField(null=True)
    date = DateField(null=False)
    is_expense = BooleanField(default=True)  # True pour une dépense, False pour un revenu
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'budgets'

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Budget, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category} - {self.amount}€ ({self.date})"

    def to_dict(self):
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