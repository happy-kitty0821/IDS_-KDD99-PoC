from django.db import models
from django.contrib.auth.models import User

class Admins(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name

class DeviceInfo(models.Model):
    HostName = models.CharField(max_length=50, primary_key=True)
    IpAddress = models.GenericIPAddressField()
    
    def __str__(self):
        return self.HostName

class PortStatus(models.Model):
    portNumber = models.BigIntegerField(unique=True, primary_key=True)
    portStatus = models.CharField(default="closed", max_length=50)
    portService = models.CharField(max_length=50)
    HostName = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.portNumber)

    
class ChangesLogs(models.Model):
    User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    DateTime = models.DateTimeField()
    HostName = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)
    ChangesDoneMessage = models.CharField(max_length=255)

    def __str__(self):
        return self.ChangesDone    

class AttacksDetected(models.Model):
    time = models.DateTimeField()
    attackType = models.CharField(max_length=200)
    pcapFileName = models.CharField(max_length=200)
    pcapLocation = models.FileField(upload_to='pcaps/')
    
    def __str__(self):
        return self.attackType