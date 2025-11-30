from django.contrib import admin
from .models import Crop, Disease, Upload

admin.site.register(Crop)
admin.site.register(Disease)
admin.site.register(Upload)
