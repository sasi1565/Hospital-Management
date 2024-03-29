# Generated by Django 4.2.1 on 2023-10-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0051_appointment_gender_approve_doctors_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Null', max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('mobileno', models.IntegerField()),
                ('message', models.CharField(max_length=400)),
            ],
        ),
        migrations.DeleteModel(
            name='contact_us_data',
        ),
    ]
