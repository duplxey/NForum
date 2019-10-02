from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='forum-index'),
    path('thread', views.thread_view, name='forum-thread'),
    path('subcategory', views.subcategory_view, name='forum-subcategory')
]