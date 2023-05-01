from django.contrib import admin
from .models import (
    Data,
    Image,
    Image2,
    Invitation,
    OneTimeUseLink,
    Doctor,
    Appointment,
    DoctorSchedule,
    DoctorAppointment,
    Feedback,
    NPS,
    Appointment2
)

# Register your models here.


class DataAdmin(admin.ModelAdmin):
    list_display = ("country", "population", "latitude", "longitude")


admin.site.register(Data, DataAdmin)
admin.site.register(Image)
admin.site.register(Image2)
admin.site.register(Invitation)
admin.site.register(OneTimeUseLink)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
admin.site.register(DoctorAppointment)
admin.site.register(Feedback)
admin.site.register(NPS)
admin.site.register(Appointment2)