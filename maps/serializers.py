from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'completed')


from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('doctor', 'client', 'appointment_time')



from .models import DoctorSchedule, DoctorAppointment

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ('doctor', 'day_of_week', 'start_time', 'break_start_time', 'break_end_time', 'end_time', 'date')

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAppointment
        fields = ('doctor', 'appointment_start_time', 'appointment_end_time')



from .models import DoctorAppointment

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAppointment
        fields = ('doctor', 'appointment_start_time', 'appointment_end_time', 'date')
