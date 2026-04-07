from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Upload

class UploadForm(forms.ModelForm):
    """
    Form to handle crop leaf image uploads with custom styling.
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

class SignUpForm(UserCreationForm):
    """
    Professional registration form for the farmers.
    """
    email = forms.EmailField(required=True, help_text="Required for account recovery.")

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user