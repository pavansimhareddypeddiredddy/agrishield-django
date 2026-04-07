from django.db import models
from django.contrib.auth.models import User

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='disease_images/', blank=True, null=True)
    cause = models.TextField(help_text="Bacterial, Fungal, Viral, or Deficiency cause.")
    symptoms = models.TextField()
    scientific_treatment = models.TextField()
    organic_treatment = models.TextField()

    def __str__(self):
        return self.name
    
class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    season = models.CharField(max_length=50)
    requirements = models.TextField(help_text="Optimal temperature, soil type, and water requirements.")
    image = models.ImageField(upload_to='crop_images/', blank=True, null=True) 
    diseases = models.ManyToManyField(Disease, related_name='affected_crops', blank=True)

    def __str__(self):
        return self.name

class Upload(models.Model):
    # Link to the User (Farmer)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Image uploaded by the farmer
    image = models.ImageField(upload_to='crop_uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # NEW: This saves the exact name from your .txt file
    predicted_disease_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Accuracy score
    confidence_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"Upload {self.id} - {self.predicted_disease_name if self.predicted_disease_name else 'Pending'}"