from django.contrib import admin
from solo.admin import SingletonModelAdmin

from home.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)
