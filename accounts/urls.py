from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='accounts-login'),
    path('signup/', views.signup, name='accounts-signup'),
    path('logout/', views.logout_view, name='accounts-logout'),
    path('home/', views.home, name='accounts-home'),
]