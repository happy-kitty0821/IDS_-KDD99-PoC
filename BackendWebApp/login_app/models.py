from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, default='defaultPP.png', upload_to='profilePictures/')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
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

    
# class ChangesLogs(models.Model):
#     User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
#     DateTime = models.DateTimeField(auto_now_add=True)
#     HostName = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)
#     ChangesDoneMessage = models.CharField(max_length=255)

#     def __str__(self):
#         return self.ChangesDone    

class AttackDetected(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    attackType = models.CharField(max_length=200)
    pcapFileName = models.CharField(max_length=200)
    pcapLocation = models.FileField(upload_to='pcaps/')
    
    def __str__(self):
        return self.attackType
    

class OTPCode(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    otpCode = models.IntegerField( null=False)
    changedOn = models.DateField(auto_now_add=True)
    isVerified = models.BooleanField(default=False)
    expireTime = models.DateTimeField(null=False)
    
    def __str__(self):
        return f"{self.username.username} - {self.otpCode}"
    
    
class SysInfo(models.Model):
    cpuUsage = models.FloatField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    ramUsage = models.FloatField(max_length=20)
    criticality = models.BooleanField(default=False)
    
    def __str__(self):
        return str(cpuUsage)