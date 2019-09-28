from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='forum-index'),
    path('thread', views.thread, name='forum-thread'),
    path('subcategory', views.subcategory, name='forum-subcategory')
]