# Generated by Django 4.2.1 on 2023-09-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0011_alter_patients_app_date_alter_patients_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='app_date',
            field=models.CharField(default='2023-09-17', max_length=20),
        ),
    ]
