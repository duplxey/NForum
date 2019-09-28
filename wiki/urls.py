from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='wiki-index'),
    path('page', views.page, name='wiki-page'),
]