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
    path('request_item/', views.request_item, name='request_item'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.change_password, name='change_password'),
    path('delete_info/', views.delete_info, name='delete_info'),
    path('item/<int:item_id>/', views.item_details, name='item_details'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]


from django.conf import settings
from django.conf.urls.static import static

# ... other URL patterns ...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)