"""
URL configuration for webbstat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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


from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from statiysate import views

urlpatterns = [
    path('', views.article, name='home'),
    path('admin/', admin.site.urls),
    path('news/<int:id>/', views.article_detail, name='article_detail'),
    path('create-article/', views.create_article, name='create_article'),
    path('edit-article/<int:id>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete_article'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('contactsnum', views.contactsnum, name='contactsnum'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<str:category>/', views.article_by_category, name='article_by_category'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name="logout"),
]
