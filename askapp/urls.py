from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('question/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('tag/', views.tag, name='tag'),
    path('hot', views.hot_view, name='hot'),
    path('settings/', views.setting, name='settings'),
    path('logout', views.logout, name='logout'),
]