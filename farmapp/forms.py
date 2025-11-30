from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):
    # This form is used to handle the user's image upload
    class Meta:
        model = Upload
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            })
        }