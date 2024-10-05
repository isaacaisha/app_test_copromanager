from django.urls import path
from .views import (
    home, register, login_view, logout_view,
    backoffice_superadmin, proposer_mise_a_jour, configurer_licence,
    dashboard_coproprietaire, dashboard_prestataire
)

# Create your urls here.

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('backoffice-superadmin/', backoffice_superadmin, name='backoffice-superadmin'),
    path('proposer-mise-a-jour/', proposer_mise_a_jour, name='proposer-mise-a-jour'),
    path('configurer-licence/<int:syndic_id>/', configurer_licence, name='configurer-licence'),
    path('dashboard-coproprietaire/', dashboard_coproprietaire, name='dashboard-coproprietaire'),
    path('dashboard-prestataire/', dashboard_prestataire, name='dashboard-prestataire'),
]