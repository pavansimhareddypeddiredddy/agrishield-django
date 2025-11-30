import os
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Upload, Disease, Crop 
from .forms import UploadForm

# --- 0. AI Model Loading (As previously discussed) ---
# NOTE: Place your actual model loading code here when ready
try:
    # Placeholder for model imports (keep commented if you don't have them installed yet)
    # from tensorflow.keras.models import load_model
    # AGRISHIELD_MODEL = load_model(os.path.join(settings.BASE_DIR, 'model.h5'))
    
    # Placeholder for class names
    CLASS_NAMES = ['Rice Blast', 'Wheat Rust', 'Healthy'] # Add all your classes here
    # print("🤖 AgriShield AI Model loaded successfully!")

except Exception as e:
    # print(f"⚠️ Error loading AI model: {e}. Running in dummy mode.")
    pass 
# ----------------------------------------------------


# --- 1. Core Page Views ---

def home(request):
    """Renders the main home page."""
    return render(request, 'farmapp/home.html')

def crops_list(request):
    """Fetches all crops from the database and orders them by name."""
    all_crops = Crop.objects.all().order_by('name') 
    context = {
        'crops': all_crops
    }
    return render(request, 'farmapp/crops.html', context)

def diseases_list(request):
    """Fetches all diseases from the database."""
    all_diseases = Disease.objects.all().order_by('name') 
    context = {
        'diseases': all_diseases
    }
    return render(request, 'farmapp/diseases.html', context)

def organic(request):
    """Renders the organic treatment information page."""
    # This view will be expanded later, but for now it renders the basic page
    return render(request, 'farmapp/organic.html')


# --- 2. Detection Logic Views ---

def upload_image(request):
    """Handles image upload and initiates the disease detection process (or dummy process)."""
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_instance = form.save(commit=False)
            
            # --- AI Detection Placeholder ---
            # NOTE: When your model is integrated, replace this block with actual prediction logic.
            predicted_name = "Tomato Leaf Spot" # Dummy prediction
            confidence_score = 98.7
            
            predicted_disease_obj = None
            try:
                # Map dummy result to a real Disease object (if it exists)
                predicted_disease_obj = Disease.objects.get(name__iexact=predicted_name)
            except Disease.DoesNotExist:
                print(f"Disease '{predicted_name}' not found in database for dummy test.")

            upload_instance.predicted_disease = predicted_disease_obj
            upload_instance.confidence_score = confidence_score
            # --------------------------------

            upload_instance.save()
            return redirect('upload_result', pk=upload_instance.pk)
    else:
        form = UploadForm()
    
    context = {
        'form': form,
        # Used to conditionally show content/messages on the upload page
        'has_diseases': Disease.objects.exists() 
    }
    return render(request, 'farmapp/upload.html', context)


def upload_result(request, pk):
    """Displays the result of the disease detection for a specific upload."""
    upload = get_object_or_404(Upload, pk=pk)
    # NOTE: The template used here must be 'farmapp/result.html'
    return render(request, 'farmapp/result.html', {'upload': upload})