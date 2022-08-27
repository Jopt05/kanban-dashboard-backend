from django.contrib import admin

# Register your models here.

from profiles import models

admin.site.register(models.UserProfile)
