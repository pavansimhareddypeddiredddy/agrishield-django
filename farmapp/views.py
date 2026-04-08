import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Upload, Disease, Crop 
from .forms import UploadForm, SignupForm

# ✅ NEW IMPORTS FOR LOGIN
from django.contrib.auth import authenticate, login


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


# --- 🔐 2. AUTHENTICATION ---

from .models import FarmerProfile

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            FarmerProfile.objects.create(
                user=user,
                age=form.cleaned_data.get("age"),
                gender=form.cleaned_data.get("gender"),
                state=form.cleaned_data.get("state"),
                district=form.cleaned_data.get("district")
            )

            return redirect("login")

        else:
            print("FORM ERRORS:", form.errors)  # DEBUG

    else:
        form = SignupForm()

    return render(request, "farmapp/signup.html", {"form": form})


# 🔥 NEW LOGIN VIEW (ADDED)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # go to home after login
        else:
            return render(request, "farmapp/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "farmapp/login.html")


# --- 3. Detection Logic Views ---

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_instance = form.save(commit=False)
            
            predicted_disease_obj = Disease.objects.first()
            
            if predicted_disease_obj:
                upload_instance.predicted_disease = predicted_disease_obj
                upload_instance.confidence_score = 99.2
                upload_instance.save()
                return redirect('upload_result', pk=upload_instance.pk) 
            else:
                return render(request, 'farmapp/upload.html', {
                    'form': form, 
                    'error': "Please add at least one Disease in the Admin Panel first!"
                })
    else:
        form = UploadForm()
    
    return render(request, 'farmapp/upload.html', {'form': form})


def upload_result(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    disease = upload.predicted_disease
    
    context = {
        'upload': upload,
        'disease': disease,
    }
    
    return render(request, 'farmapp/result.html', context)

from django.contrib.auth.decorators import login_required
from .models import FarmerProfile

@login_required
def profile_view(request):
    user = request.user
    
    try:
        profile = FarmerProfile.objects.get(user=user)
    except FarmerProfile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'farmapp/profile.html', context)

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')