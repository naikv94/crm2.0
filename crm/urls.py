"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from crm import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from api import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #Authentication Urls
    path('register/', views.registerView, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='common/login.html'
        ),
        name='login'
    ),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
        ),
        name='logout'
    ),

    ## Dashboard URLs
    path('companies/', views.companyView, name='companies'),
    path('deleteCompany/<int:id>/', views.companyDeleteView, name='deleteCompany'),
    path('updateCompany/<int:id>/', views.companyUpdateView, name='updateCompany'),

    path('contacts/', views.contactView, name='contacts'),
    path('deleteContact/<int:id>/', views.contactDeleteView, name='deleteContact'),
    path('updateContact/<int:id>/', views.contactUpdateView, name='updateContact'),

    path('accounts/profile/', views.profile, name='profile'),
    path('profileUpdate/', views.profileUpdate, name='profileUpdate'),

    path('change-password/',auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    ################# Password Reset #####################
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='common/password-reset/password_reset.html'
    ), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='common/password-reset/password_reset_done.html'
    ), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='common/password-reset/password_reset_confirm.html'
    ), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='common/password-reset/password_reset_email.html'
    ), name ='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
