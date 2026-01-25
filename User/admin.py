from django.contrib import admin

# Register your models here.
from .models import User, Weeks 
admin.site.register(User)
admin.site.register(Weeks)