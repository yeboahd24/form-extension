from django.db import models
import geocoder
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.


class Data(models.Model):
    country = models.CharField(max_length=100, null=True)
    population = models.PositiveIntegerField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Data"

    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.country).lat
        self.longitude = geocoder.osm(self.country).lng
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.country


class Image(models.Model):
    image = models.ImageField(upload_to="images/")


class Image2(models.Model):
    image_file = ProcessedImageField(
        upload_to="uploads/",
        processors=[ResizeToFit(width=800, height=600)],
        format="JPEG",
        options={"quality": 60},
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Invitation(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return self.email


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#import PermissionsMixin
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


from django.contrib.auth import get_user_model
#import timezone
from django.utils import timezone

User = get_user_model()


class OneTimeUseLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    expiration_time = models.DateTimeField()


    def is_expired(self):
        return timezone.now() > self.expiration_time



class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)


class Recording(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='recordings/')



class File(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    zip_file = models.FileField(upload_to='zip/')

    def __str__(self):
        return self.uploaded_file.name




class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any other relevant fields for the doctor

    def __str__(self):
        return self.user.email

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_time = models.DateField()
    # Add any other relevant fields for the appointment

    def __str__(self):
        return f"{self.doctor.user.email} with {self.client.email}"





class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    break_start_time = models.TimeField()
    break_end_time = models.TimeField()
    end_time = models.TimeField()
    date =  models.DateField(blank=True, null=True)

class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    date =  models.DateField(blank=True, null=True)