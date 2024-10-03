from django.shortcuts import render
from datetime import datetime


def mainModule(request):
    context = {
        'date': datetime.now().strftime("%a %d %B %Y")
        }

    return render(request, 'base/main_module.html', context)
