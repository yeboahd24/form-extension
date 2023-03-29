"""crimemap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from maps.views import index, file_upload, image_upload, image_uploads, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="map"),
    path("file_upload/", file_upload, name="file_upload"),
    path("image_upload/", image_upload, name="image_upload"),
    path("image_uploads/", image_uploads, name="image_uploads"),
    path("weather/", home, name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
