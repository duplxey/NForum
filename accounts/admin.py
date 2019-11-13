from django.contrib import admin
from accounts.models import Profile, Alert, Achievement, UserAchievement

admin.site.register(Profile)
admin.site.register(Alert)
admin.site.register(Achievement)
admin.site.register(UserAchievement)

