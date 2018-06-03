'''
Created on 2018. 6. 2.

@author: 1104-5
'''
from django.urls import path
from .views import *
app_name = 'blog'
urlpatterns = [
    path('',index,name='index'),
    path('<int:post_id>/', detail, name='detail'),
    path('posting/', posting, name='posting'),
    path('delete/<int:post_id>/', post_delete,name='delete'),
    path('update/<int:post_id>/', post_update,name='update'),
    ]