from cgitb import text
from django.shortcuts import render
from .models import Data
import folium
from folium import plugins
from .forms import MyForm
from django.http import HttpResponse
from .forms import ImageForm, ImageForm2
from .models import Image, Image2
import requests

# Create your views here.


def index(request):
    data = Data.objects.all()
    data_list = Data.objects.values_list("latitude", "longitude", "population")

    map1 = folium.Map(location=[19, -12], tiles="CartoDB Dark_Matter", zoom_start=2)

    plugins.HeatMap(data_list).add_to(map1)
    plugins.Fullscreen(position="topright").add_to(map1)
    plugins.LocateControl().add_to(map1)  # get current location
    plugins.BeautifyIcon(icon="fa fa-leaf").add_to(map1)
    map1 = map1._repr_html_()
    context = {"map1": map1}
    return render(request, "map.html", context)


def file_upload(request):
    if request.method == "POST":
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            return HttpResponse("File Uploaded Successfully")
    else:
        form = MyForm()
    return render(request, "file_upload.html", {"form": form})


def image_upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist("image")
            for image in images:
                Image.objects.create(image=image)
            # Redirect to a success page here
            return HttpResponse("File Uploaded Successfully")
    else:
        form = ImageForm()
    return render(request, "image_upload.html", {"form": form})


def image_uploads(request):
    if request.method == "POST":
        form = ImageForm2(request.POST, request.FILES)
        if form.is_valid():
            image_files = request.FILES.getlist("image_file")
            for image_file in image_files:
                Image2.objects.create(image_file=image_file)
            # Redirect to a success page here
            return HttpResponse("File Uploaded Successfully")

        else:
            print(form.errors)
    else:
        form = ImageForm2()
    return render(request, "image_uploads.html", {"form": form})


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=3c7c773669d848278185995171e95f3a&units=metric"
    response = requests.get(url)
    data = response.json()
    if "main" in data and "weather" in data:
        weather = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        return weather
    else:
        return None


def home(request):
    city = "London"  # default city
    if "city" in request.GET:
        city = request.GET["city"]
    weather = get_weather(city)
    context = {
        "weather": weather,
    }
    return render(request, "weather.html", context)


# def stock_exchange(request):
#     key = "TCY1KXE31773M772"
#     url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey={key}"
#     response = requests.get(url)
#     data = response.json()
#     context = {
#         "symbol": data["Global Quote"]["01. symbol"],
#         "buying_amount": data["Global Quote"]["05. price"],
#         "selling_amount": data["Global Quote"]["08. previous close"],
#         "country_flag": "flags/US.png",
#     }
#     return render(request, "stock_exchange.html", context)


def exchange_rates(request):
    countries = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "NZD"]
    rates = []
    key = "TCY1KXE31773M772"
    for country in countries:
        response = requests.get(
            f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={country}&to_currency=USD&apikey={key}"
        )
        data = response.json()
        if "Realtime Currency Exchange Rate" in data:
            rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            rates.append((country, rate))
    context = {"rates": rates}
    return render(request, "exchange_rates.html", context)


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Invitation
from django.utils.crypto import get_random_string


def invite(request):
    if request.method == "POST":
        email = request.POST.get("email")
        token = get_random_string(length=32)
        invitation = Invitation.objects.create(email=email, token=token)
        if invitation is None:
            return redirect("error")
        invitation_url = request.build_absolute_uri(f"/accept/{token}/")
        send_mail(
            "Invitation to join our website",
            f"You have been invited to join our website. Click on the following link to accept the invitation: {invitation_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect("success")
    return render(request, "invite.html")


def accept(request, token):
    invitation = Invitation.objects.filter(token=token).first()
    if invitation is None:
        return redirect("error")
    if invitation.status != "pending":
        return redirect("error")
    invitation.status = "accepted"
    invitation.save()
    send_mail(
        "Invitation Accepted",
        f"The invitation sent to {invitation.email} has been accepted.",
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )
    return redirect("success", status="accepted", email=invitation.email)


def success(request, status=None, email=None):
    if status == "accepted":
        message = f"Thank you for accepting the invitation. You can now log in using your email address: {email}."
    elif status == "declined":
        message = "Thank you for letting us know that you cannot join us at this time."
    else:
        message = "Your invitation has been sent. Please check your email for further instructions."
    return render(request, "success.html", {"message": message})


def error(request):
    return render(request, "error.html")


def decline(request):
    token = request.GET.get("token")
    invitation = Invitation.objects.filter(token=token).first()
    if invitation and invitation.status == "pending":
        invitation.status = "declined"
        invitation.save()
        return redirect("success", status="declined", email=invitation.email)
    return redirect("error")


from django.views.generic import FormView
from django.urls import reverse_lazy
import json

from .forms import ContactForm


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def form_valid(self, form):
        # Add code to handle the form submission
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        # print the error
        print(form.errors)


def contact_success(request):
    return render(request, "contact_success.html")


from django.contrib import messages


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            messages.success(
                request,
                "Thank you for contacting us! We will get back to you as soon as possible.",
            )
            return redirect("contact_success")
        else:
            if not form.cleaned_data.get("phone_number"):
                messages.error(request, "Please enter a phone number.")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


from django.http import JsonResponse
from .forms import MyForm


def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = MyForm()
    return render(request, "captcha_form.html", {"form": form})


# from captcha.helpers import captcha_image_url
# from captcha.models import CaptchaStore

# def refresh_captcha(request):
#     if request.is_ajax():
#         new_captcha = CaptchaStore.generate_key()
#         image_url = captcha_image_url(new_captcha)
#         response_data = {'image_url': image_url, 'key': new_captcha}
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Invalid request'})


from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore


@require_GET
@csrf_exempt
def refresh_captcha(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        new_key = CaptchaStore.generate_key()
        to_json_response = {
            "key": new_key,
            "image_url": captcha_image_url(new_key),
            "audio_url": captcha_audio_url(new_key),
        }
        return JsonResponse(to_json_response)
    else:
        return HttpResponseBadRequest()


from django.shortcuts import render, redirect
from django.core.signing import TimestampSigner, BadSignature
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import OneTimeUseLink
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


def generate_one_time_use_link(user):
    signer = TimestampSigner()
    link = signer.sign(user.email)
    expiration_time = timezone.now() + timezone.timedelta(minutes=5)
    OneTimeUseLink.objects.create(user=user, link=link, expiration_time=expiration_time)
    return link


# def send_one_time_use_link(user, link):
#     subject = 'Your one-time use login link'
#     message = f'Click this link to log in: <a href="{link}">{link}</a>'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user.email]
#     send_mail(subject, message, from_email, recipient_list, html_message=message)


def send_one_time_use_link(user, link):
    domain = "localhost:8000"  # Replace with your domain name and port number
    path = f"/login/{link}/"
    url = f"http://{domain}{path}"
    subject = "Your one-time use login link"
    message = f'Click this link to log in: <a href="{url}">{url}</a>'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, html_message=message)


def login_with_one_time_use_link(request, link):
    try:
        signer = TimestampSigner()
        email = signer.unsign(link, max_age=300)
        user = User.objects.get(email=email)
        one_time_use_link = OneTimeUseLink.objects.get(
            user=user, link=link, expiration_time__gte=timezone.now()
        )
        one_time_use_link.delete()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        return render(request, "login_success.html")
    except (ValueError, BadSignature, User.DoesNotExist, OneTimeUseLink.DoesNotExist):
        return render(request, "login_failure.html")


def login_with_email(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
            link = generate_one_time_use_link(user)
            send_one_time_use_link(user, link)
            return redirect("check_email")
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email address"})
    else:
        return render(request, "login.html")


def check_email(request):
    return render(request, "check_email.html")


from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer

class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


def todo(request):
    return render(request, "todo.html")



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Todo
from .serializers import TodoSerializer

@csrf_exempt
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from dal import autocomplete

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')



class TaskAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Task.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs



from django.http import JsonResponse
from maps.models import Recording
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_recording(request):
    if request.method == 'POST':
        recording = Recording()
        recording.audio_file = request.FILES['audio_file']
        recording.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})



@csrf_exempt
def record(request):
    return render(request, 'record.html')




from django.shortcuts import render, redirect
from django.http import HttpResponse
import zipfile
from .models import File
from django.core.files.uploadhandler import TemporaryFileUploadHandler
import zipfile
import tempfile


def download_file(request, pk):
    file = File.objects.get(pk=pk)
    response = HttpResponse(file.zip_file.read())
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = f'attachment; filename="{file.uploaded_file.name}.zip"'
    return response



def zip_files(file_list):
    with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip, 'w') as zip_file:
            for f in file_list:
                with TemporaryFileUploadHandler(f, None) as handler:
                    handler.file_name = f.name
                    uploaded_file = handler.file.file
                    zip_file.write(uploaded_file.name, uploaded_file.name)
    return temp_zip.name

def upload_file(request):
    if request.method == 'POST':
        file_list = request.FILES.getlist('file')
        temp_files = []
        for uploaded_file in file_list:
            with TemporaryFileUploadHandler(uploaded_file, None) as handler:
                handler.file_name = uploaded_file.name
                temp_file = handler.file.file
                temp_files.append(temp_file)
        zip_file_path = zip_files(temp_files)
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            # save the zip file in the response as the name of the original file
            response['Content-Disposition'] = f'attachment; filename="file.zip"'
            return response
    return render(request, 'upload_file.html')








from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django import forms
from formtools.wizard.views import SessionWizardView
class ContactForm1(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField()

class ContactForm2(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

class ContactWizard(SessionWizardView):
    form_list = [ContactForm1, ContactForm2]
    template_name = 'contact_form.html'
    success_url = '/done/'

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)
        return render(self.request, 'done.html', {'form_data': form_data})

def process_form_data(form_list):
    form_data = [form.cleaned_data for form in form_list]
    return form_data

def home_view(request):
    return render(request, 'home.html', {})

def done(request):
    return render(request, 'done.html', {})



from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .todo import todos

def index(request):
    return render(request, 'index.html', {'todos': []})

@require_http_methods(['POST'])
def search(request):
    res_todos = []
    search = request.POST['search']
    if len(search) == 0:
        return render(request, 'todo2.html', {'todos': []})
    for i in todos:
        if search in i['title']:
            res_todos.append(i)
    return render(request, 'todo2.html', {'todos': res_todos})
