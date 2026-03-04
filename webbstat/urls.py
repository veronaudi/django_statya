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
from statiysate import views
from statiysate import api_views

urlpatterns = [
    path('', views.article, name='home'),
    path('admin/', admin.site.urls),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
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
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name="logout"),

    path('api/articles/', api_views.api_article_list, name='api_article_list'),
    path('api/articles/<int:id>/', api_views.api_article_detail, name='api_article_detail'),
    path("api/articles/create/", api_views.api_create_article),
    path("api/articles/<int:id>/update/", api_views.api_update_article),
    path("api/articles/<int:id>/delete/", api_views.api_delete_article),
    path("api/articles/category/<str:category>/", api_views.api_articles_by_category),
    path("api/articles/sort/date/", api_views.api_articles_sorted_by_date),

    path("api/comment/", api_views.comment_list),
    path("api/comment/<int:id>/", api_views.comment_detail),
    path("api/comment/create/", api_views.comment_create),
    path("api/comment/<int:id>/update/", api_views.comment_update),
    path("api/comment/<int:id>/delete/", api_views.comment_delete),
    path("api/token/", api_views.token_obtain),
    path("api/token/refresh/", api_views.token_refresh),



]
