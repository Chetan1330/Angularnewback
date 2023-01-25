from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=100, blank=True)
    picture = models.ImageField(upload_to='profile_pics', blank=True)

# class Userform(AbstractUser):
#     fullname = models.CharField(max_length=200, blank=True)
#     email = models.CharField(max_length=200, blank=True)
#     password = models.CharField(max_length=200, blank=True)

class ScenarioUser(models.Model):
    user_id = models.CharField(max_length=200, blank=True)
    
class Scenario(models.Model):
    user=models.ForeignKey(ScenarioUser, on_delete=models.CASCADE, related_name='Scenario')
    response_data=models.JSONField(null=True)
    # ScenarioName= models.CharField(max_length=100, blank=True)
    # ModelLinks= models.CharField(max_length=200, blank=True)
    # LinktoDataset= models.CharField(max_length=200, blank=True)
    # Description= models.CharField(max_length=200, blank=True)

class ScenarioSolution(models.Model):
    user=models.ForeignKey(ScenarioUser, on_delete=models.CASCADE, related_name='scenariosolution')
    ScenarioName= models.CharField(max_length=100, blank=True)
    SolutionName= models.CharField(max_length=200, blank=True)
    SolutionDescription= models.CharField(max_length=200, blank=True)

    TrainingFile = models.FileField(upload_to='files', blank=True, null = True)
    TestFile = models.FileField(upload_to='files', blank=True, null = True)
    FactsheetFile = models.FileField(upload_to='files', blank=True, null = True)
    ModelFile = models.FileField(upload_to='files', blank=True, null = True)

    Targetcolumn= models.CharField(max_length=200, blank=True)
    

class FirstStock(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    form_data=models.JSONField(null=True)
    response_data=models.JSONField(null=True)

class SecondStock(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    form_data=models.JSONField(null=True)
    response_data=models.JSONField(null=True)
    
    
    
