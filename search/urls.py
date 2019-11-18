from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_fail_view, name='search-search'),
    path('<str:keyword>/', views.search_view, name='search-search'),
]
