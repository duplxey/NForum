from django.contrib import admin
from solo.admin import SingletonModelAdmin

from settings.models import SiteConfiguration, SiteSocialNetwork, SiteColorPalette

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(SiteColorPalette, SingletonModelAdmin)
admin.site.register(SiteSocialNetwork)
