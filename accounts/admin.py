from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from models import UserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    raw_id_fields = ("editor_for",)

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


# Register your models here.
admin.site.register(User, UserProfileAdmin)
