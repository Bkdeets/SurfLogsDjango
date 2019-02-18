from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Spot(models.Model):
    name =                  models.CharField(max_length=200, primary_key=True)
    ideal_wind =            models.CharField(max_length=200)
    ideal_tide =            models.CharField(max_length=200)
    ideal_wind =            models.CharField(max_length=200)
    ideal_swell_dir	=       models.IntegerField(default=0)
    ideal_swell_height =    models.IntegerField(default=0)
    ideal_swell_period =    models.IntegerField(default=0)
    type =                  models.CharField(max_length=200)
    location =              models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Wave_Data(models.Model):
    wave_data_id =  models.AutoField(primary_key=True)
    date =          models.DateTimeField('date')
    time = 	        models.TimeField('time')
    spot =          models.ForeignKey(Spot, on_delete=models.CASCADE)
    tide =          models.CharField(max_length=200)
    crowd =         models.CharField(max_length=200)
    wind_dir =      models.CharField(max_length=200)
    wave_height =   models.IntegerField(default=0)
    wave_period =   models.CharField(max_length=200)
    wind_speed =    models.CharField(max_length=200)
    conditions =    models.CharField(max_length=200)

class Session(models.Model):
    session_id =     models.AutoField(primary_key=True)
    date =           models.DateTimeField('session date')
    start_time =     models.TimeField('start time')
    end_time = 	     models.TimeField('end time')
    wave_data_id =   models.ForeignKey(Wave_Data, on_delete=models.CASCADE)
    spot =           models.ForeignKey(Spot, on_delete=models.CASCADE)
    user =           models.ForeignKey(User, on_delete=models.CASCADE)
    notes =          models.CharField(max_length=200)
    waves_caught = 	 models.IntegerField(default=0)
    rating =         models.IntegerField(default=0)
    #photos =          models.ImageField(upload_to=self.get_image_path, blank=True, null=True)

    def __str__(self):
        return "Session at " + self.spot.name + " from " + str(self.start_time) + " to " + str(self.end_time) + " on " + str(self.date) + "."

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

class Profile(models.Model):
    user =          models.OneToOneField(User, on_delete=models.CASCADE)
    bio =           models.TextField(max_length=500, blank=True)
    homespot =      models.ForeignKey(Spot, on_delete=models.CASCADE, blank=True, null=True)
    #photo =             models.ImageField(upload_to=self.get_image_path, blank=True, null=True)

class Report(models.Model):
    report_id =    models.AutoField(primary_key=True)
    date =         models.DateTimeField('report date')
    time = 	       models.TimeField('time')
    spot =         models.ForeignKey(Spot, on_delete=models.CASCADE)
    conditions =   models.CharField(max_length=200)
    user =         models.ForeignKey(User, on_delete=models.CASCADE)
    notes =        models.CharField(max_length=200)
    wave_quality = models.CharField(max_length=200)
        #photos =          models.ImageField(upload_to=self.get_image_path, blank=True, null=True)

    def __str__(self):
        return "Report: " + self.spot.name + " at " + str(self.time) + " on " + str(self.date) + "."


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(instance)
    print(kwargs)
    print(created)
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
