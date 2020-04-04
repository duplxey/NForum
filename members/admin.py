from django.contrib import admin
from .models import UserProfile, Alert, Achievement, UserAchievement

admin.site.register(UserProfile)
admin.site.register(Alert)
admin.site.register(Achievement)
admin.site.register(UserAchievement)

