"""
URL configuration for capstone_project project.
"""
from django.contrib import admin
from django.urls import path, include

# CRITICAL IMPORTS FOR MEDIA FILES:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('farmapp.urls')),
]

# CRITICAL BLOCK: This serves media files (user uploads) only when DEBUG=True
# This is required for images to display on the Crops page.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)