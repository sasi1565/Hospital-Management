# Generated by Django 4.2.1 on 2023-10-20 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0057_remove_feedback_data_mobileno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='doctor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HospitalManagement.doctorreg'),
        ),
        migrations.AlterField(
            model_name='discharged_patients',
            name='address',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
