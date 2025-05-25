from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel

class Budget(BaseModel):
    """Modèle pour les budgets"""
    id_budget = AutoField(primary_key=True)
    name_budget = CharField(max_length=100)
    start_amount_budget = DecimalField(max_digits=12, decimal_places=2, default=0)
    end_amount_budget = DecimalField(max_digits=12, decimal_places=2, null=True)
    date_creation_budget = DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.name_budget
    
    @property
    def remaining_amount(self):
        """Calcule le montant restant"""
        if self.end_amount_budget is not None:
            return self.start_amount_budget - self.end_amount_budget
        return self.start_amount_budget
    
    @property
    def spent_amount(self):
        """Calcule le montant dépensé"""
        if self.end_amount_budget is not None:
            return self.end_amount_budget
        return 0
    
    def add_expense(self, amount):
        """Ajoute une dépense au budget"""
        if self.end_amount_budget is None:
            self.end_amount_budget = amount
        else:
            self.end_amount_budget += amount
        self.save()
    
    def is_exceeded(self):
        """Vérifie si le budget est dépassé"""
        return self.end_amount_budget and self.end_amount_budget > self.start_amount_budget