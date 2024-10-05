from django import forms
from .models import Licence
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


# Formulaire d'inscription
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        #exclude = ['host', 'participants']


# Formulaire de connexion (vous pouvez utiliser celui de Django)
class LoginForm(AuthenticationForm):
    pass


class LicenceForm(forms.ModelForm):
    class Meta:
        model = Licence
        fields = ['date_debut', 'date_fin', 'statut', 'options_specifiques']
