#utils.py file of login_app
import netifaces as ni
import socket
import pyotp
import psutil
import threading
import time
from django.core.mail import send_mail
from django.conf import settings
from .models import DeviceInfo, PortStatus, SysInfo
from django.conf import settings
from datetime import datetime, timedelta 



def sendEmail(email, username, password):
    subject = "Account Created Successfully"
    message = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Created Successfully</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
        }}

        .footer {{
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Account Created Successfully</h1>
        <p>Dear User,</p>
        <p>Your account has been created successfully. Below are your account details:</p>
        <ul>
            <li><strong>Username:</strong> {username}</li>
            <li><strong>Password:</strong> {password}</li>
            <li><strong>Email:</strong> {email}</li>
        </ul>
        <p>Please do not share this email with anyone. All the alerts and security verification code will be sent to this email.</p>
        <p class="footer">This is an automated email. Please do not reply.</p>
    </div>
</body>
</html>

    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, from_email, recipient_list, html_message=message)
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


def getAndStoreIp():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface == 'lo':
            continue
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            ip_address = addresses[ni.AF_INET][0]['addr']
            hostname = socket.gethostname()
            if hostname is None:
                continue
            # Check if the IP address and hostname are already stored means it reurns true
            AlreadyStore = DeviceInfo.objects.filter(HostName=hostname, IpAddress=ip_address).exists()
            print(f"is it already stored?? {AlreadyStore}")
            if AlreadyStore == False:# Save the IP address and hostname in the DeviceInfo model if it returns false
                DeviceInfo.objects.all().delete()#delete all the rows
                #after deleting create a new row
                DeviceInfo.objects.create(HostName=hostname, IpAddress=ip_address)
            return hostname, ip_address
    return None, None  # Return None if no non-loopback interface is found

hostname, ipAddress = getAndStoreIp()
if hostname and ipAddress:
    print(f"Hostname: {hostname}, IP Address: {ipAddress}")
else:
    print("No non-loopback interface found")
    
def getServiceName(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

def scanPorts():
    hostname, ip_address = getAndStoreIp()
    if hostname is None:
        print("No hostname found")
        return
    
    # Retrieve the DeviceInfo instance for the host
    try:
        device_info = DeviceInfo.objects.get(HostName=hostname)
    except DeviceInfo.DoesNotExist:
        print(f"DeviceInfo with HostName {hostname} does not exist")
        return
        # Delete all existing PortStatus records for the current host
    PortStatus.objects.all().delete()
    for port in range(1, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)  # Timeout for socket connection
            result = s.connect_ex((ip_address, port))
            if result == 0:
                service_name = getServiceName(port)
                port_status = PortStatus(portNumber=port, portStatus="open", portService=service_name, HostName=device_info)
                port_status.save()
                print(f"-----------------------------")
                print(f"Port {port}: {service_name}")

# Get hostname and IP address
hostname, ipAddress = getAndStoreIp()

# Print hostname and IP address
if hostname and ipAddress:
    print(f"Hostname: {hostname}, IP Address: {ipAddress}")
else:
    print("No non-loopback interface found")

# Scan ports
host = ipAddress
scanPorts()

def sendOTPMail(otp, userEmail):
    subject="OTP for password change"
    message = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OTP Email</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        p {{
            color: #666;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 10px;
        }}
        span.otp {{
            color: #ff0000;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Your OTP is: <span class="otp">{ otp }</span></h2>
        <p>Please use this OTP to verify your email address.</p>
        <p>If you didn't request this OTP, please ignore this email.</p>
        <p>Thank you!</p>
    </div>
</body>
</html>

"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [userEmail]
    try:
        send_mail(subject, message, from_email, recipient_list, html_message=message)
    except Exception as e:
        print(f"An error occurred while sending email: {e}")



# def getCpuRamUsage():
#     while True:
#         cpuUsage = psutil.cpu_times_percent(interval=.5)
#         ramUsage = psutil.virtual_memory()
#         print(f"cpu usage is {cpuUsage}")
#         print(f"ram usage is {ramUsage}")
#         yield cpuUsage, ramUsage #use yield insted of return to send the dadta continously




def updateSysinfo():
    while True:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram_percent = psutil.virtual_memory().percent
        criticalityStatus = cpu_percent >= 80
        SysInfo.objects.create(cpuUsage=cpu_percent, ramUsage=ram_percent, criticality=criticalityStatus)
        print(f"CPU Usage: {cpu_percent}%")
        time.sleep(300)  #waiting for 300 seconds (5 minute)

# Start the thread
update_thread = threading.Thread(target=updateSysinfo)
update_thread.daemon = True  # Daemonize the thread so it stops when the main process stops
update_thread.start()
