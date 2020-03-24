from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='wiki-index'),

    path('add/', views.page_add, name='wiki-page-add'),
    path('change/<slug:url>/', views.page_change, name='wiki-page-change'),
    path('delete/<slug:url>/', views.page_delete, name='wiki-page-delete'),

    # Due to no prefix, this URL needs to be first.
    path('<slug:url>/', views.page_view, name='wiki-page'),
]