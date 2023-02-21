from django.urls import path
from assets import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'assets'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home_page'),
    path('login/', auth_views.LoginView.as_view(template_name='assets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='assets/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('request/', views.request_item, name='request_item'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.change_password, name='change_password'),
    path('claim/<int:id>/', views.claim, name='claim'),
]
