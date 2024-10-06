from django.contrib import admin
from .models import CustomUser, Licence, Document

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Licence)
admin.site.register(Document)
