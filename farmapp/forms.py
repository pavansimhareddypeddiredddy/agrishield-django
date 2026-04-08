from django import forms
from .models import Upload

# ✅ Existing Upload Form (DON'T TOUCH)
class UploadForm(forms.ModelForm):
    """
    Form to handle crop leaf image uploads for disease detection.
    """
    class Meta:
        model = Upload
        fields = ['image']
        
        labels = {
            'image': ''
        }
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'accept': 'image/*',
                'id': 'image_input',
                'onchange': 'previewImage(this);'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large! Please upload an image smaller than 5MB.")
        return image


#  SIGNUP FORM
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FarmerProfile

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.IntegerField()

    gender = forms.ChoiceField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])

    state = forms.CharField(max_length=100)
    district = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "age",
            "gender",
            "state",
            "district"
        ]
        # email validation
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists! Try logging in.")

        return email