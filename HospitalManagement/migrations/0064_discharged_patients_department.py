# Generated by Django 4.2.1 on 2023-10-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0063_discharged_patients_app_or_pat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discharged_patients',
            name='department',
            field=models.CharField(default='Cardiologist', max_length=100, null=True),
        ),
    ]
