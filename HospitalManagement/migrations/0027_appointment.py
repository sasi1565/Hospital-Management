# Generated by Django 4.2.1 on 2023-10-04 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0026_delete_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255, null=True)),
                ('lastname', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('age', models.CharField(max_length=3, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('symptoms', models.CharField(max_length=400, null=True)),
                ('department', models.CharField(default='NUll', max_length=20, null=True)),
                ('description', models.TextField(max_length=200, null=True)),
            ],
        ),
    ]
