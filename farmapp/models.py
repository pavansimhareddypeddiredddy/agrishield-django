from django.db import models
from django.contrib.auth.models import User  # ✅ IMPORTANT


class Disease(models.Model):
    crop = models.ForeignKey(
        'Crop',
        on_delete=models.CASCADE,
        related_name='disease_list'  # 👈 changed name to avoid future conflicts
    )

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='diseases/')
    cause = models.TextField()
    symptoms = models.TextField()
    scientific_treatment = models.TextField()
    organic_treatment = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.crop.name})"

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    season = models.CharField(max_length=50)
    requirements = models.TextField(help_text="Optimal temperature, soil type, and water requirements.")
    
    image = models.ImageField(upload_to='crop_images/', blank=True, null=True) 
    
    diseases = models.ManyToManyField(Disease, related_name='affected_crops', blank=True)

    def __str__(self):
        return self.name


class Upload(models.Model):
    image = models.ImageField(upload_to='crop_uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    predicted_disease = models.ForeignKey(
        Disease, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='predictions'
    )
    confidence_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"Upload {self.id} - {self.predicted_disease.name if self.predicted_disease else 'Pending'}"


# 🔥 NEW MODEL (ADD THIS)
class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
    
    
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("Email already exists!")