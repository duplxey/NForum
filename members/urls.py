from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='members-login'),
    path('signup/', views.signup_view, name='members-signup'),
    path('logout/', views.logout_view, name='members-logout'),

    path('members/', views.members_view, name='members-members'),

    path('profile/<str:username>/', views.profile_specific_view, name='members-profile'),
    path('alert/', views.alert_view, name='members-alert'),
    path('achievement/', views.achievement_view, name='members-achievement'),
    path('settings/', views.settings_view, name='members-settings'),
]