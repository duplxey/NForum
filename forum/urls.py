from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='forum-index'),
    path('thread/<str:thread_title>', views.thread_view, name='forum-thread'),
    path('thread-create/<str:subcategory_name>', views.thread_create_view, name='forum-thread-create'),
    path('thread-reply/<str:thread_title>', views.thread_post_view, name='forum-thread-reply'),
    path('message-edit/<str:message_id>', views.message_edit_view, name='forum-message-edit'),
    path('message-remove/<str:message_id>', views.message_remove_view, name='forum-message-remove'),
    path('message-upvote/<str:message_id>', views.message_upvote, name='forum-message-upvote'),
    path('message-downvote/<str:message_id>', views.message_downvote, name='forum-message-downvote'),
    path('subcategory/<str:subcategory_name>', views.subcategory_view, name='forum-subcategory'),
]
