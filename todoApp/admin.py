from django.contrib import admin
from .models import ToDone
# Register your models here.


class ToDoneAdmin(admin.ModelAdmin):
    list_display = ('sn', 'user' 'title', 'description', 'date')
    

admin.site.register(ToDone)