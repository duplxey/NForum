from django.contrib import admin
from accounts.models import Profile, Alert, AlertType

admin.site.register(Profile)
admin.site.register(AlertType)
admin.site.register(Alert)