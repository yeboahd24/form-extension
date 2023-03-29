from cgitb import text
from django.shortcuts import render
from .models import Data
import folium
from folium import plugins
from .forms import MyForm
from django.http import HttpResponse
from .forms import ImageForm, ImageForm2
from .models import Image, Image2

# Create your views here.


def index(request):
    data = Data.objects.all()
    data_list = Data.objects.values_list('latitude', 'longitude', 'population')

    map1 = folium.Map(location=[19, -12],
                      tiles='CartoDB Dark_Matter', zoom_start=2)


    plugins.HeatMap(data_list).add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    plugins.LocateControl().add_to(map1) # get current location
    plugins.BeautifyIcon(icon='fa fa-leaf').add_to(map1) 
    map1 = map1._repr_html_()
    context = {
        'map1': map1
    }
    return render(request, 'map.html', context)



def file_upload(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            return HttpResponse('File Uploaded Successfully')
    else:
        form = MyForm()
    return render(request, 'file_upload.html', {'form': form})


def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            for image in images:
                Image.objects.create(image=image)
            # Redirect to a success page here
            return HttpResponse('File Uploaded Successfully')
    else:
        form = ImageForm()
    return render(request, 'image_upload.html', {'form': form})



def image_uploads(request):
    if request.method == 'POST':
        form = ImageForm2(request.POST, request.FILES)
        if form.is_valid():
            image_files = request.FILES.getlist('image_file')
            for image_file in image_files:
                Image2.objects.create(image_file=image_file)
            # Redirect to a success page here
            return HttpResponse('File Uploaded Successfully')

       
        else:
            print(form.errors)
    else:
        form = ImageForm2()
    return render(request, 'image_uploads.html', {'form': form})
