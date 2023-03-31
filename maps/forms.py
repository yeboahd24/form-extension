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
        fields = ("image",)
        widgets = {
            "image": forms.ClearableFileInput(attrs={"multiple": True}),
        }


class ImageForm2(forms.ModelForm):
    class Meta:
        model = Image2
        fields = ("image_file",)
        widgets = {
            "image_file": forms.ClearableFileInput(attrs={"multiple": True}),
        }


from django import forms
from phonenumber_field.formfields import PhoneNumberField

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_number.country_code = self.cleaned_data.get('phone_number_country_code')
            return phone_number
        return None


from captcha.fields import CaptchaField

class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()