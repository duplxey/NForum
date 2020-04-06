"""nforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from forum import views as f_views

admin.site.site_header = "NForum"
admin.site.site_title = "Welcome to the Control Panel."
admin.site.index_title = "Welcome to the Control Panel."

urlpatterns = [
    path('', f_views.home_view, name='index'),
    path('forum/', include('forum.urls')),
    path('search/', include('search.urls')),
    path('wiki/', include('wiki.urls')),
    path('members/', include('members.urls')),
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
