# Generated by Django 4.2.1 on 2023-10-18 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0054_appointment_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
    ]
