from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='wiki-index'),
    path('<str:url>/', views.page_view, name='wiki-page'),
]