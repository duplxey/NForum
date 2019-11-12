from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='accounts-login'),
    path('signup/', views.signup_view, name='accounts-signup'),
    path('logout/', views.logout_view, name='accounts-logout'),

    path('members/', views.members_view, name='accounts-members'),

    path('profile/<str:username>/', views.profile_specific_view, name='accounts-profile'),
    path('alert/', views.alert_view, name='accounts-alert'),
    path('settings', views.settings_view, name='accounts-settings'),
]