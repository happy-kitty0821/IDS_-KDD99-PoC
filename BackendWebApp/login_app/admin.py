from django.contrib import admin
from .models import DeviceInfo, PortStatus, AttackDetected, OTPCode, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture']
admin.site.register(Profile, ProfileAdmin)

 
class DeviceInfoAdmin(admin.ModelAdmin):
     list_display = ('HostName', 'IpAddress')
     search_fields = ('HostName', 'IpAddress')
admin.site.register(DeviceInfo, DeviceInfoAdmin)

class PortStatusAdmin(admin.ModelAdmin):
     list_display = ('portNumber', 'portStatus', 'portService', 'HostName')
     search_fields = ('portNumber', 'portService', 'HostName__HostName')
admin.site.register(PortStatus, PortStatusAdmin)

# class ChangesLogsAdmin(admin.ModelAdmin):
#      list_display = ('User', 'DateTime', 'HostName', 'ChangesDoneMessage')
#      search_fields = ('User__username', 'HostName__HostName', 'ChangesDoneMessage')
#      list_filter = ('DateTime',)
# admin.site.register(ChangesLogs, ChangesLogsAdmin)
 
class AttackDetectedAdmin(admin.ModelAdmin):
     list_display = ('time', 'attackType', 'pcapFileName', 'pcapLocation')
     search_fields = ('attackType', 'pcapFileName')
     list_filter = ('time',)
admin.site.register(AttackDetected, AttackDetectedAdmin)


#@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('username', 'otpCode', 'changedOn', 'isVerified', 'expireTime')

admin.site.register(OTPCode, OTPCodeAdmin)