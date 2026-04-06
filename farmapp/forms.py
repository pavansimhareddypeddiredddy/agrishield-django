from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):
    """
    Form to handle crop leaf image uploads for disease detection.
    """
    class Meta:
        model = Upload
        fields = ['image']
        
        labels = {
            'image': '' # Leave blank to use the custom 'Click to upload' box in your HTML
        }
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control d-none', # 'd-none' hides the ugly default button
                'accept': 'image/*',
                'id': 'image_input',  # Crucial for your JavaScript preview
                'onchange': 'previewImage(this);' # Triggers the preview immediately
            })
        }

    def clean_image(self):
        """
        Validates the file size to ensure it's not too large 
        (Safe for your 1Gi AWS EBS Volume).
        """
        image = self.cleaned_data.get('image')
        if image:
            # Check if file is larger than 5MB
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large! Please upload an image smaller than 5MB.")
        return image