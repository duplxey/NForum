from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='wiki-index'),
    path('add/', views.page_add, name='wiki-page-add'),
    path('change/<str:url>/', views.page_change, name='wiki-page-change'),
    path('delete/<str:url>/', views.page_delete, name='wiki-page-delete'),
    path('<str:url>/', views.page_view, name='wiki-page'),
]