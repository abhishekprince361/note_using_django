from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('new_note/', views.new_note, name='new_note'),
    path('all_notes/', views.all_notes, name='all_notes'),
    path('user_home/', views.user_home, name='user_home'),
    path('search/', views.search, name='search'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]