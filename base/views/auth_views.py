# auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from datetime import datetime


# View for registration
def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('backoffice-superadmin')
        else:
            print('error register')

    return render(request, 'base/register.html', {'form': form})


# View for login
def login_view(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        return handle_login(request, form)

    context = {
        'form': form,
        'date': datetime.now().strftime("%a %d %B %Y")
    }

    return render(request, 'base/login.html', context)


def handle_login(request, form):
    """Handles user authentication and redirection based on user role."""
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)

        # Redirect to the next URL if available, else go to home
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)

        return redirect_based_on_role(user)

    return render(request, 'base/login.html', {'form': form, 'error': 'Invalid credentials.'})


def redirect_based_on_role(user):
    """Redirects users based on their roles."""
    role_redirects = {
        'superadmin': 'backoffice-superadmin',
        'syndic': 'configurer-licence',
        'coproprietaire': 'dashboard-coproprietaire',
        'prestataire': 'dashboard-prestataire',
    }

    # Redirect syndic with the necessary syndic_id argument
    if user.role == 'syndic':
        return redirect('configurer-licence', syndic_id=user.id)

    # For other roles, simply redirect to the appropriate dashboard
    return redirect(role_redirects.get(user.role, 'home'))


# View for logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
