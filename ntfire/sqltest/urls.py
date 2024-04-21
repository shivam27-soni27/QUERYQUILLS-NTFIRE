from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('process_form', views.process_form, name='process_form'),
    path('upload', views.upload_file, name='upload_file'),
    path('execute_query', views.execute_query, name='execute_query'),
]
