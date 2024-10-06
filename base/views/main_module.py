# views.py
import shutil
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from base.models import CustomUser, Licence
from base.forms import LicenceForm
from datetime import datetime,date


def home(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y")
    }
    return render(request, 'base/home.html', context)


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
