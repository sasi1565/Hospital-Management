# Generated by Django 4.2.1 on 2023-10-20 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0060_remove_discharged_patients_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='discharged_patients',
        ),
    ]
