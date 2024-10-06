from .auth_views import register, login_view, logout_view

from .main_module import home, configurer_licence, dashboard_coproprietaire, dashboard_prestataire

from .utils_main_module import backoffice_superadmin, proposer_mise_a_jour, creer_dossier_syndic, mettre_a_jour_dossier_syndic

from ..templatetags.form_filters import add_class
