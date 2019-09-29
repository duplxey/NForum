from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='wiki-index'),
    path('page/<str:url>/', views.page, name='wiki-page'),
]