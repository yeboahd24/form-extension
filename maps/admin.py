from django.contrib import admin
from .models import Data, Image, Image2, Invitation,OneTimeUseLink

# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ('country', 'population', 'latitude', 'longitude')


admin.site.register(Data, DataAdmin)
admin.site.register(Image)
admin.site.register(Image2)
admin.site.register(Invitation)
admin.site.register(OneTimeUseLink)