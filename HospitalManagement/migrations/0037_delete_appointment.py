# Generated by Django 4.2.1 on 2023-10-05 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0036_rename_date_created_appointment_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]