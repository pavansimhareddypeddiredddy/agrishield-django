from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    # --- CRITICAL FIX: Add the image field for the Admin Panel ---
    image = models.ImageField(upload_to='disease_images/', blank=True, null=True)
    # -----------------------------------------------------------
    
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
    
    # CRITICAL ADDITION: Image field for crop photo
    image = models.ImageField(upload_to='crop_images/', blank=True, null=True) 
    
    diseases = models.ManyToManyField(Disease, related_name='affected_crops', blank=True)

    def __str__(self):
        return self.name

class Upload(models.Model):
    # This model tracks images uploaded by the user
    image = models.ImageField(upload_to='crop_uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # AI Prediction Results
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