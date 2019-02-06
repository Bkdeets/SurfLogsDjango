from django.db import models
import os
#from .models import Spot,User,Session,Report

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


class User(models.Model):
    username =          models.CharField(max_length=200, primary_key=True)
    firstname =         models.CharField(max_length=200)
    lastname =          models.CharField(max_length=200)
    about =             models.CharField(max_length=200)
    #photo =             models.ImageField(upload_to=self.get_image_path, blank=True, null=True)
    homespot =          models.ForeignKey(Spot, on_delete=models.CASCADE)
    securityQuestion =  models.CharField(max_length=200)
    securityAnswer =    models.CharField(max_length=200)
    email =             models.CharField(max_length=200)
    password =          models.CharField(max_length=200)
    created =           models.DateTimeField('date created')

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

    def __str__(self):
        return self.firstname + " " + self.lastname

class Report(models.Model):
    report_id =   models.AutoField(primary_key=True)
    date =        models.DateTimeField('session date')
    time = 	      models.TimeField('end time')
    spot =        models.ForeignKey(Spot, on_delete=models.CASCADE)
    tide =        models.CharField(max_length=200)
    conditions =  models.CharField(max_length=200)
    user =        models.ForeignKey(User, on_delete=models.CASCADE)
    notes =       models.CharField(max_length=200)
    crowd =       models.CharField(max_length=200)
    wind_dir =    models.CharField(max_length=200)

    def __str__(self):
        return "Report: " + self.spot.name + " at " + str(self.time) + " on " + str(self.date) + "."

class Session(models.Model):
    session_id =     models.AutoField(primary_key=True)
    date =           models.DateTimeField('session date')
    start_time =     models.TimeField('start time')
    end_time = 	     models.TimeField('end time')
    report_id =      models.ForeignKey(Report, on_delete=models.CASCADE)
    spot =           models.ForeignKey(Spot, on_delete=models.CASCADE)
    user =           models.ForeignKey(User, on_delete=models.CASCADE)
    notes =          models.CharField(max_length=200)
    waves_caught = 	 models.IntegerField(default=0)
    rating =         models.IntegerField(default=0)
    #photo =          models.ImageField(upload_to=self.get_image_path, blank=True, null=True)

    def __str__(self):
        return "Session at " + self.spot.name + " from " + str(self.start_time) + " to " + str(self.end_time) + " on " + str(self.date) + "."

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)
