import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Upload, Disease, Crop 
from .forms import UploadForm, SignupForm

# ✅ NEW IMPORTS FOR LOGIN
from django.contrib.auth import authenticate, login

# ✅ AI MODEL IMPORT
from .ai_model_loader import predict_disease, solutions


# --- 1. Core Page Views ---

def home(request):
    return render(request, 'farmapp/home.html')

def crops_list(request):
    all_crops = Crop.objects.all().order_by('name') 
    return render(request, 'farmapp/crops.html', {'crops': all_crops})

from django.shortcuts import render
from django.db.models import Q
from .models import Disease


def diseases(request):
    query = request.GET.get('q', '').strip()

    diseases = Disease.objects.select_related('crop').all()

    if query:
        query_clean = query.replace(" ", "_")

        diseases = diseases.filter(
            Q(name__icontains=query) |
            Q(name__icontains=query_clean) |
            Q(crop__name__icontains=query)
        )

    context = {
        'diseases': diseases,
        'query': query
    }

    return render(request, 'farmapp/diseases.html', context)

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
            print("FORM ERRORS:", form.errors)

    else:
        form = SignupForm()

    return render(request, "farmapp/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "farmapp/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "farmapp/login.html")


# --- 🚀 3. AI Detection Logic ---

def upload_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            upload_instance = form.save(commit=False)
            upload_instance.save()

            image_path = upload_instance.image.path

            # 🔥 AI PREDICTION
            disease_name, confidence = predict_disease(image_path)

            # Convert to lowercase (VERY IMPORTANT)
            disease_name_lower = disease_name.lower()

            # 🚨 NOT A LEAF
            if confidence < 0.40:
                disease_name = "non_leaf"
                crop_status = "Not a leaf detected"

            elif disease_name_lower == "other_leaf":
                crop_status = "Crop not found in database"

            elif disease_name_lower == "non_leaf":
                crop_status = "Not a leaf detected"

            else:
                # ✅ HANDLE BOTH ___ AND _
                if "___" in disease_name:
                    crop_name = disease_name.split("___")[0]
                elif "_" in disease_name:
                    crop_name = disease_name.split("_")[0]
                else:
                    crop_name = "unknown"

                crop_name = crop_name.lower()  # normalize

                if Crop.objects.filter(name__iexact=crop_name).exists():
                    crop_status = "Crop Found"
                else:
                    crop_status = "Crop not found in database"

            # ✅ STORE IN SESSION
            request.session['disease'] = disease_name
            request.session['confidence'] = confidence * 100  # fix % issue
            request.session['crop_status'] = crop_status

            return redirect('upload_result', pk=upload_instance.pk)

    else:
        form = UploadForm()

    return render(request, 'farmapp/upload.html', {'form': form})

def upload_result(request, pk):
    upload = get_object_or_404(Upload, pk=pk)

    # 🔥 GET AI RESULT
    disease_name = request.session.get('disease', 'Unknown')
    confidence = request.session.get('confidence', 0)
    crop_status = request.session.get('crop_status', 'N/A')  # ✅ ADD THIS

    # 🔥 GET SOLUTION FROM JSON
    disease_data = solutions.get(disease_name, {})

    context = {
        'upload': upload,
        'disease_name': disease_name,
        'confidence': confidence,
        'crop_status': crop_status,   # ✅ ADD THIS
        'symptoms': "No symptoms available",
        'scientific_cure': ", ".join(disease_data.get('scientific', [])),
        'organic_cure': ", ".join(disease_data.get('organic', [])),
    }

    return render(request, 'farmapp/result.html', context)


# --- 👤 PROFILE ---

from django.contrib.auth.decorators import login_required

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


# --- 🚪 LOGOUT ---

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')