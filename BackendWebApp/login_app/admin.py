from django.contrib import admin
from .models import Admins, DeviceInfo, PortStatus, ChangesLogs, AttacksDetected
class AdminsAdmin(admin.ModelAdmin):
     list_display = ('name', 'phone', 'email', 'date_created')
     search_fields = ('name', 'phone', 'email')
     list_filter = ('date_created',)
admin.site.register(Admins, AdminsAdmin)
 
class DeviceInfoAdmin(admin.ModelAdmin):
     list_display = ('HostName', 'IpAddress')
     search_fields = ('HostName', 'IpAddress')
admin.site.register(DeviceInfo, DeviceInfoAdmin)

class PortStatusAdmin(admin.ModelAdmin):
     list_display = ('portNumber', 'portStatus', 'portService', 'HostName')
     search_fields = ('portNumber', 'portService', 'HostName__HostName')
admin.site.register(PortStatus, PortStatusAdmin)
class ChangesLogsAdmin(admin.ModelAdmin):
     list_display = ('User', 'DateTime', 'HostName', 'ChangesDoneMessage')
     search_fields = ('User__username', 'HostName__HostName', 'ChangesDoneMessage')
     list_filter = ('DateTime',)
admin.site.register(ChangesLogs, ChangesLogsAdmin)
 
class AttacksDetectedAdmin(admin.ModelAdmin):
     list_display = ('time', 'attackType', 'pcapFileName', 'pcapLocation')
     search_fields = ('attackType', 'pcapFileName')
     list_filter = ('time',)
admin.site.register(AttacksDetected, AttacksDetectedAdmin)