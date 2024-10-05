# views.py
import shutil
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base.models import CustomUser, Licence
from base.forms import RegisterForm, LoginForm, LicenceForm
from django.contrib.auth import login, authenticate, logout
from datetime import datetime,date


# # Créer des utilisateurs avec différents rôles
# CustomUser.objects.create_user(username='syndic1', email='syndic1@mail.com', password='password123', role='syndic')
# CustomUser.objects.create_user(username='coproprietaire1', email='copro1@mail.com', password='password123', role='coproprietaire')
# CustomUser.objects.create_user(username='prestataire1', email='prestataire1@mail.com', password='password123', role='prestataire')


# # Create test users in your shell or migration
# def create_test_users():
#     roles = ['superadmin', 'syndic', 'coproprietaire', 'prestataire']
#     for role in roles:
#         CustomUser.objects.create_user(
#             username=f'{role}1', 
#             email=f'{role}1@mail.com', 
#             password='password123', 
#             role=role
#         )

#form_licence = LicenceForm()
#print(form_licence.as_p())  # This will display the form fields as HTML

syndic = CustomUser.objects.get(id=1)
print(syndic.username)  # Ensure this prints the expected username


# For creaating folders
def creer_dossier_syndic(nom_syndic):
    modele_dossier = '/chemin/vers/modele_syndic'
    nouveau_dossier = f'/chemin/vers/syndics/{nom_syndic}'

    if not os.path.exists(nouveau_dossier):
        shutil.copytree(modele_dossier, nouveau_dossier)
        print(f"Dossier créé pour le syndic : {nom_syndic}")
    else:
        print(f"Le dossier pour le syndic {nom_syndic} existe déjà.")


# For updating existing folders
def mettre_a_jour_dossier_syndic(nom_syndic, nouvelle_version):
    chemin_syndic = f'/chemin/vers/syndics/{nom_syndic}'
    nouveau_modele = f'/chemin/vers/modele_syndic_{nouvelle_version}'

    if os.path.exists(chemin_syndic):
        for item in os.listdir(nouveau_modele):
            s = os.path.join(nouveau_modele, item)
            d = os.path.join(chemin_syndic, item)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print(f"Dossier de {nom_syndic} mis à jour vers la version {nouvelle_version}")
    else:
        print(f"Dossier pour le syndic {nom_syndic} introuvable.")


# Vue pour l'inscription
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print('error register')
    else:
        form = RegisterForm()

    return render(request, 'base/register.html', {'form': form})


# Vue pour la connexion
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                # Redirect to the next URL if available, else go to home
                #next_url = request.GET.get('next')
                #if next_url:
                #    return redirect(next_url)
                
                # Role-based redirection
                if user.role == 'superadmin':
                    return redirect('backoffice-superadmin')
                elif user.role == 'syndic':
                    return redirect('configurer-licence', syndic_id=user.id)
                elif user.role == 'coproprietaire':
                    return redirect('dashboard-coproprietaire')  # Add the correct view for coproprietaire dashboard
                elif user.role == 'prestataire':
                    return redirect('dashboard-prestataire')  # Add the correct view for prestataire dashboard
                else:
                    return redirect('home')  # Default redirection if no role matches
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'date': datetime.now().strftime("%a %d %B %Y")
    }

    return render(request, 'base/login.html', context)


# Vue pour la déconnexion
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y")
    }
    return render(request, 'base/home.html', context)


@user_passes_test(lambda user: user.role == 'superadmin')
def backoffice_superadmin(request):
    syndics = CustomUser.objects.filter(role='syndic')
    coproprietaires = CustomUser.objects.filter(role='coproprietaire')
    prestataires = CustomUser.objects.filter(role='prestataire')

    return render(request, 'base/backoffice_superadmin.html', {
        'syndics': syndics,
        'coproprietaires': coproprietaires,
        'prestataires': prestataires,
    })

@login_required
#@user_passes_test(lambda user: user.role == 'superadmin')
def proposer_mise_a_jour(request, syndic_id, nouvelle_version):
    syndic = get_object_or_404(CustomUser, id=syndic_id, role='syndic')
    licence = get_object_or_404(Licence, syndic=syndic)

    mettre_a_jour_dossier_syndic(syndic.username, nouvelle_version)
    licence.version_dossier = nouvelle_version
    licence.save()

    return redirect('backoffice-superadmin')


#@user_passes_test(lambda user: user.role == 'superadmin')
def configurer_licence(request, syndic_id):
    syndic = get_object_or_404(CustomUser, id=syndic_id, role='syndic')
    
    # Set default values for required fields
    default_date_debut = date.today()  # For example, today’s date
    default_date_fin = date(default_date_debut.year + 1, default_date_debut.month, default_date_debut.day)  # One year from now
    default_statut = 'active'  # Assuming you want new licences to start as 'active'

    # Ensure required fields are set when creating a new Licence
    licence, created = Licence.objects.get_or_create(
        syndic=syndic,
        defaults={
            'date_debut': default_date_debut,
            'date_fin': default_date_fin,
            'statut': default_statut,
        }
    )

    if request.method == 'POST' and created:
        form = LicenceForm(request.POST, instance=licence)
        if form.is_valid():
            form.save()
            return redirect('backoffice-superadmin')
    else:
        form = LicenceForm(instance=licence)

    return render(request, 'base/configurer_licence.html', {'form': form, 'syndic': syndic})


@login_required
def dashboard_coproprietaire(request):
    """
    View for the coproprietaire dashboard.
    This view should display information relevant to coproprietaires, 
    such as co-owner documents, charges, and announcements.
    """
    # Add any necessary context for coproprietaire-specific data
    context = {
        'username': request.user.username,
        'date': datetime.now().strftime("%a %d %B %Y")
        # Add more relevant context data here, e.g., user-specific documents
    }
    return render(request, 'base/dashboard_coproprietaire.html', context)


@login_required
def dashboard_prestataire(request):
    """
    View for the prestataire dashboard.
    This view should display information relevant to prestataires,
    such as assigned tasks, projects, or service requests.
    """
    # Add any necessary context for prestataire-specific data
    context = {
        'username': request.user.username,
        'date': datetime.now().strftime("%a %d %B %Y")
        # Add more relevant context data here, e.g., service requests
    }
    return render(request, 'base/dashboard_prestataire.html', context)
