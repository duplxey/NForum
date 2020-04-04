from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import *


admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Thread)
admin.site.register(ThreadPrefix)

admin.site.register(ForumConfiguration, SingletonModelAdmin)
