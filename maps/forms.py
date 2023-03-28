from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator


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
