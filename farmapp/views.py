import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Upload, Disease, Crop 
from .forms import UploadForm

# --- 1. Core Page Views ---

def home(request):
    return render(request, 'farmapp/home.html')

def crops_list(request):
    all_crops = Crop.objects.all().order_by('name') 
    return render(request, 'farmapp/crops.html', {'crops': all_crops})

def diseases_list(request):
    all_diseases = Disease.objects.all().order_by('name') 
    return render(request, 'farmapp/diseases.html', {'diseases': all_diseases})

def organic(request):
    return render(request, 'farmapp/organic.html')


# --- 2. Detection Logic Views ---

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_instance = form.save(commit=False)
            
            # --- AGRI-SHIELD LOGIC ---
            # For your B.Tech Demo: We pick the first disease available in your Admin panel
            # to simulate a successful detection. 
            # Later, your AI model code will go here.
            
            predicted_disease_obj = Disease.objects.first() # Grabs the first disease you added
            
            if predicted_disease_obj:
                upload_instance.predicted_disease = predicted_disease_obj
                upload_instance.confidence_score = 99.2 # High confidence for the demo!
                upload_instance.save()
                # Use 'upload' (the name in your URL pattern) instead of 'upload_result'
                return redirect('upload_result', pk=upload_instance.pk) 
            else:
                # If you haven't added any diseases in Admin yet
                return render(request, 'farmapp/upload.html', {
                    'form': form, 
                    'error': "Please add at least one Disease in the Admin Panel first!"
                })
    else:
        form = UploadForm()
    
    return render(request, 'farmapp/upload.html', {'form': form})


def upload_result(request, pk):
    """Fetches the specific upload and its diagnosis."""
    upload = get_object_or_404(Upload, pk=pk)
    
    # We get the disease object from the upload record
    disease = upload.predicted_disease
    
    context = {
        'upload': upload,
        'disease': disease,
    }
    
    return render(request, 'farmapp/result.html', context)