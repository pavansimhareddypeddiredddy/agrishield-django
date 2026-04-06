from django.urls import path
from . import views

# This variable MUST be named exactly 'urlpatterns'
# It must be a LIST [ ], which is the 'iterable' Django is looking for.
urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Information Lists
    path('crops/', views.crops_list, name='crops'),
    path('diseases/', views.diseases_list, name='diseases'),
    path('organic/', views.organic, name='organic'),
    
    # Detection Process
    path('upload/', views.upload_image, name='upload'),
    
    # Result Page - Note: 'upload_result' matches the redirect in your views.py
    path('result/<int:pk>/', views.upload_result, name='upload_result'),
]