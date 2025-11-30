from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),
    
    # CROPS (Use the functional view that fetches data)
    path('crops/', views.crops_list, name='crops'),
    
    # DISEASES (Use the functional view that fetches data)
    path('diseases/', views.diseases_list, name='diseases'),
    
    # ORGANIC
    path('organic/', views.organic, name='organic'),
    
    # UPLOAD - Handles image submission
    path('upload/', views.upload_image, name='upload'),
    
    # RESULT - Requires the primary key (pk) of the upload record
    path('result/<int:pk>/', views.upload_result, name='upload_result'),
]