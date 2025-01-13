from django.contrib import admin
from .models import User


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'bio')

admin.site.register(User)
