from django.contrib import admin

from .models import *


admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Thread)
admin.site.register(ThreadPrefix)
