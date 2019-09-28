from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thread', views.thread, name='thread'),
    path('subcategory', views.subcategory, name='subcategory')
]