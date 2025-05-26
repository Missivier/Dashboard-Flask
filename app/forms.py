from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, DateField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange

class RegisterForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class CreateHouseForm(FlaskForm):
    name_house = StringField('Nom de la maison', validators=[DataRequired()])
    adress = StringField('Adresse', validators=[Optional()])
    description_house = TextAreaField('Description', validators=[Optional()])
    photo_house = StringField('Photo (URL)', validators=[Optional()])
    submit = SubmitField('Créer la maison')

class ProfileForm(FlaskForm):
    name_user = StringField('Nom', validators=[DataRequired()])
    first_name_user = StringField('Prénom', validators=[DataRequired()])
    username_user = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    phone_user = StringField('Téléphone', validators=[Optional()])
    age_user = IntegerField('Âge', validators=[Optional()])
    date_birthday_user = DateField('Date de naissance', validators=[Optional()])
    email_user = StringField('Email', validators=[DataRequired(), Email()])
    description_user = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Enregistrer les modifications')

class TaskForm(FlaskForm):
    """Formulaire pour la création et modification de tâches"""
    name_task = StringField('Nom de la tâche', validators=[DataRequired(), Length(max=200)])
    description_task = TextAreaField('Description')
    status = SelectField('Statut', coerce=int)
    list_task = SelectField('Liste', coerce=int)
    submit = SubmitField('Enregistrer')

class ListTaskForm(FlaskForm):
    """Formulaire pour la création et modification de listes de tâches"""
    name_list_task = StringField('Nom de la liste', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Enregistrer') 

class PetForm(FlaskForm):
    name = StringField('Nom', validators=[
        DataRequired(message="Le nom est requis"),
        Length(min=2, max=100, message="Le nom doit contenir entre 2 et 100 caractères")
    ])
    
    species = SelectField('Espèce', validators=[DataRequired(message="L'espèce est requise")], 
                         choices=[
                             ('chien', 'Chien'),
                             ('chat', 'Chat'),
                             ('oiseau', 'Oiseau'),
                             ('rongeur', 'Rongeur'),
                             ('autre', 'Autre')
                         ])
    
    breed = StringField('Race', validators=[
        Optional(),
        Length(max=50, message="La race ne doit pas dépasser 50 caractères")
    ])
    
    birth_date = DateField('Date de naissance', validators=[Optional()])
    
    weight = FloatField('Poids (kg)', validators=[
        Optional(),
        NumberRange(min=0, max=100, message="Le poids doit être compris entre 0 et 100 kg")
    ])
    
    submit = SubmitField('Enregistrer') 

class BudgetForm(FlaskForm):
    name = StringField('Nom du budget', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Catégorie', choices=[
        ('nourriture', 'Nourriture'),
        ('veterinaire', 'Vétérinaire'),
        ('accessoires', 'Accessoires'),
        ('toilettage', 'Toilettage'),
        ('assurance', 'Assurance'),
        ('autre', 'Autre')
    ], validators=[DataRequired()])
    amount = FloatField('Montant (€)', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    date = DateField('Date', validators=[DataRequired()])
    is_expense = BooleanField('Dépense', default=True)

class TestForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer') 