from django.contrib import admin

# Register your models here.
from .models import recipe # Import your model

# Register your model here
admin.site.register(recipe)
