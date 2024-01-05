# Generated by Django 4.2.1 on 2023-10-18 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0055_remove_appointment_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HospitalManagement.doctorreg'),
        ),
    ]