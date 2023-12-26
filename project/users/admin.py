import django.contrib.auth.models
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin

import users.models


class ProfileAdmin(TabularInline):
    model = users.models.Profile
    can_delete = False


class USerAdmin(UserAdmin):
    inlines = (ProfileAdmin,)


django.contrib.admin.site.register(users.models.User, USerAdmin)
