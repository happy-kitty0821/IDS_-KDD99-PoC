# Generated by Django 5.0.2 on 2024-03-25 07:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttackDetected',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('attackType', models.CharField(max_length=200)),
                ('pcapFileName', models.CharField(max_length=200)),
                ('pcapLocation', models.FileField(upload_to='pcaps/')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('HostName', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('IpAddress', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Hawa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hawa', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChangesLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateTime', models.DateTimeField(auto_now_add=True)),
                ('ChangesDoneMessage', models.CharField(max_length=255)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('HostName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_app.deviceinfo')),
            ],
        ),
        migrations.CreateModel(
            name='OtpTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otpCode', models.IntegerField()),
                ('isVerified', models.BooleanField(default=False)),
                ('expireTime', models.DateTimeField()),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PortStatus',
            fields=[
                ('portNumber', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('portStatus', models.CharField(default='closed', max_length=50)),
                ('portService', models.CharField(max_length=50)),
                ('HostName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_app.deviceinfo')),
            ],
        ),
    ]
