from django.contrib import admin
from solo.admin import SingletonModelAdmin

from home.models import SiteConfiguration, SiteSocialNetwork

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(SiteSocialNetwork)
