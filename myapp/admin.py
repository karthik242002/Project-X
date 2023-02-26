from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Feature,Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Feature)
