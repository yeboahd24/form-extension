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
