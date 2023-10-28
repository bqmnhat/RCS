from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bod = models.DateTimeField('Birth of Date')
    address = models.CharField('Home Address',max_length=20)
    city = models.CharField('City',max_length=20)
    phone = models.IntegerField('Phone number')
    created_at = models.DateTimeField('Date Created')
    pic = models.ImageField("Picture",upload_to=user_directory_path,blank=True)

    def __str__(self):
        return self.user.username

class Specialist(models.Model):
    description = models.CharField('Description',max_length=50)
    def __str__(self):
        return self.description

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bod = models.DateTimeField('Birth of Date')
    address = models.CharField('Home Address',max_length=20)
    city = models.CharField('City',max_length=20)
    phone = models.IntegerField('Phone number')
    created_at = models.DateTimeField('Date Created')
    pic = models.ImageField("Picture",upload_to=user_directory_path,blank=True)
    specialist = models.ForeignKey(Specialist, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PatientRecord(models.Model):
    description = models.CharField('Short description',max_length=100)
    heart_rate = models.IntegerField('Heart rate value')
    blood_pressure = models.IntegerField('Blood pressure vallue')
    temperature = models.FloatField('Temperature value')
    symptom = models.TextField('symptoms',blank=True)
    image1 = models.ImageField(upload_to = user_directory_path)
    image2 = models.ImageField(upload_to = user_directory_path)
    image3 = models.ImageField(upload_to = user_directory_path)
    created_at = models.DateTimeField('date published')
    patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)

class Prescription(models.Model):
    medicine = models.CharField('Medicine name',max_length=50)
    quantity = models.IntegerField('quantity')
    usage = models.CharField('Usage instruction', max_length=150)
    patient_record = models.ForeignKey(PatientRecord, blank=True, null=True, on_delete=models.CASCADE)

class TimeTable(models.Model):
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    slot_duration = models.IntegerField('Duration of each slot');
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)

class Slot(models.Model):
    start_time = models.DateTimeField('Slot Start time')
    end_time = models.DateTimeField('Slot End time')
    video_link = models.URLField(max_length = 200) 
    time_table = models.ForeignKey(TimeTable, blank=True, null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.CASCADE)