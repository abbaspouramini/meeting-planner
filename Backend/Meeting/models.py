from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Meeting(models.Model):
    ownerID = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ownermeet',null=True)
    users = models.ManyToManyField(to=User,through='UserMeet',related_name='meetusers')
    title = models.CharField(max_length=256)
    duration = models.TimeField()
    phone_number = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=400,blank=True)
    Language_Choices = [
        ('PE', 'Persian'),
        ('EN', 'English'),
    ]
    language = models.CharField(max_length=2,choices=Language_Choices,default='EN')
    message = models.CharField(max_length=400)
    url = models.CharField(max_length=128,unique=True)
    color = models.CharField(max_length=100)
    finaltime = models.DateTimeField(null=True)
    Time_Status_Choices = [
        ('Ch', 'Choosing'),
        ('Fn', 'Finalized'),
    ]
    timestatus = models.CharField(max_length=2, choices=Time_Status_Choices, default='Ch')


class UserMeet(models.Model):
    meetID= models.ForeignKey(to=Meeting,on_delete=models.CASCADE)
    userID= models.ForeignKey(to=User,on_delete=models.CASCADE)



class AvailableTimes(models.Model):
    userid= models.ForeignKey(to=UserMeet,on_delete=models.CASCADE)
    date_time = models.DateTimeField()



class OwnerAvailableTimes(models.Model):
    meetID = models.ForeignKey(to=Meeting, on_delete=models.CASCADE)
    Day_of_Week = [
        ('Sat','Saturday'),
        ('Sun','Sunday'),
        ('Mon','Monday'),
        ('Tue','Tuesday'),
        ('Wen','Wendsday'),
        ('Thu','Thursday'),
        ('Fri','Friday')]
    day = models.CharField(max_length=3,choices=Day_of_Week,default='Sat')
    startTime = models.TimeField()
    endTime = models.TimeField()