from django.db import models

# Create your models here.
class ClassRoom(models.Model):  
    name = models.CharField(max_length=30)  
    tutor = models.CharField(max_length=30)  
  
class Student(models.Model):  
    name = models.CharField(max_length=30)  
    sex = models.CharField(max_length=5)  
    age = models.IntegerField()  
    state_province = models.CharField(max_length=30)  
    qq = models.IntegerField()  
    classroom = models.ForeignKey(ClassRoom)  