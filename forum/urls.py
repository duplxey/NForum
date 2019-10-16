from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='forum-index'),
    path('thread/<str:thread_title>', views.thread_view, name='forum-thread'),
    path('thread-create/<str:subcategory_name>', views.thread_create_view, name='forum-thread-create'),
    path('subcategory/<str:subcategory_name>', views.subcategory_view, name='forum-subcategory'),
]
