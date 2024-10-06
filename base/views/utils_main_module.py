# utils_main_module.py
import shutil
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base.models import CustomUser, Licence
from datetime import datetime


@user_passes_test(lambda user: user.role == 'superadmin')
def backoffice_superadmin(request):
    syndics = CustomUser.objects.filter(role='syndic')
    coproprietaires = CustomUser.objects.filter(role='coproprietaire')
    prestataires = CustomUser.objects.filter(role='prestataire')

    context = {
        'syndics': syndics,
        'coproprietaires': coproprietaires,
        'prestataires': prestataires,
        'username': request.user.username,
        'date': datetime.now().strftime("%a %d %B %Y")
    }

    return render(request, 'base/backoffice_superadmin.html', context)


@login_required
#@user_passes_test(lambda user: user.role == 'superadmin')
def proposer_mise_a_jour(request, syndic_id, nouvelle_version):
    syndic = get_object_or_404(CustomUser, id=syndic_id, role='syndic')
    licence = get_object_or_404(Licence, syndic=syndic)

    mettre_a_jour_dossier_syndic(syndic.username, nouvelle_version)
    licence.version_dossier = nouvelle_version
    licence.save()

    return redirect('backoffice-superadmin')


# For creaating folders
def creer_dossier_syndic(nom_syndic):
    modele_dossier = '/chemin/vers/modele_syndic'
    nouveau_dossier = f'/chemin/vers/syndics/{nom_syndic}'

    if not os.path.exists(nouveau_dossier):
        shutil.copytree(modele_dossier, nouveau_dossier)
        print(f"Dossier créé pour le syndic : {nom_syndic}")
    else:
        print(f"Le dossier pour le syndic {nom_syndic} existe déjà.")


# Function for updating existing folders
def mettre_a_jour_dossier_syndic(nom_syndic, nouvelle_version):
    chemin_syndic = f'/chemin/vers/syndics/{nom_syndic}'
    nouveau_modele = f'/chemin/vers/modele_syndic_{nouvelle_version}'

    # Check if the syndic folder exists
    if not os.path.exists(chemin_syndic):
        print(f"Dossier pour le syndic {nom_syndic} introuvable.")
        return

    # Check if the new model folder exists before proceeding
    if not os.path.exists(nouveau_modele):
        print(f"Dossier modèle pour la version {nouvelle_version} introuvable.")
        return

    # Update the syndic folder with the new model
    for item in os.listdir(nouveau_modele):
        s = os.path.join(nouveau_modele, item)
        d = os.path.join(chemin_syndic, item)
        if os.path.isdir(s):
            if not os.path.exists(d):
                shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    print(f"Dossier de {nom_syndic} mis à jour vers la version {nouvelle_version}")
