from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index_view, name='home-index'),
]