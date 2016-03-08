from django.contrib import admin
from userprofile.models import UserProfile
from django.contrib import admin

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "steamURL", "joined_at")
    ordering = ("user",)
