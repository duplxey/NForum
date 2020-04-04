from django.urls import path

from . import views

urlpatterns = [
    path('', views.forum_view, name='forum-index'),

    path('thread/<str:thread_title>/', views.thread_view, name='forum-thread'),
    path('thread-create/<str:subcategory_name>/', views.thread_create_view, name='forum-thread-create'),
    path('thread-reply/<str:thread_title>/', views.thread_post_view, name='forum-thread-reply'),

    path('message-edit/<str:message_id>/', views.message_edit_view, name='forum-message-edit'),
    path('message-remove/<str:message_id>/', views.message_remove_view, name='forum-message-remove'),
    path('message-rate/', views.message_rate, name='forum-message-rate'),

    path('subcategory/<str:subcategory_name>/', views.subcategory_view, name='forum-subcategory'),
]
