from django.urls import path

from askme import views

urlpatterns = [

    path('', views.index, name='index'),
    path('question/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('tag/', views.tag, name='tag'),
]