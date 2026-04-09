from django.urls import path
from . import views
from .views import signup_view
from .views import login_view
from .views import home
from .views import profile_view

# This variable MUST be named exactly 'urlpatterns'
# It must be a LIST [ ], which is the 'iterable' Django is looking for.
urlpatterns = [
    # Home Page
    path('', signup_view, name='home'),
    # Information Lists
    path('crops/', views.crops_list, name='crops'),
    path('diseases/', views.diseases, name='diseases'),
    path('organic/', views.organic, name='organic'),
    
    # Detection Process
    path('upload/', views.upload_image, name='upload'),
    
    # Result Page - Note: 'upload_result' matches the redirect in your views.py
    path('result/<int:pk>/', views.upload_result, name='upload_result'),
    
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]