from django.urls import path
from .views import (
    mainModule
)

# Create your urls here.

urlpatterns = [
    #path('login/', loginPage, name='login'),
    #path('logout/', logoutUser, name='logout'),
    #path('register/', registerPage, name='register'),

    path('', mainModule, name='main-module')
]