from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator
from .models import Image, Image2


class MyForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={"multiple": True}),
        validators=[
            FileExtensionValidator(allowed_extensions=settings.ALLOWED_EXTENSIONS)
        ],
    )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise forms.ValidationError("The file is too large.")
        return file




class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class ImageForm2(forms.ModelForm):
    class Meta:
        model = Image2
        fields = ('image_file',)
        widgets = {
            'image_file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
