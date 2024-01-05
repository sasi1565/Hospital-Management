# Generated by Django 4.2.1 on 2023-10-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0020_doctors_image_alter_discharged_patients_app_date_and_more'),
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
                ('status', models.CharField(choices=[('pending', 'pending'), ('booked', 'booked')], default='pending', max_length=100)),
                ('age', models.CharField(max_length=3, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('symptoms', models.CharField(max_length=400, null=True)),
                ('description', models.TextField(max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='discharged_patients',
            name='app_date',
            field=models.CharField(default='2023-10-01', max_length=20),
        ),
        migrations.AlterField(
            model_name='discharged_patients',
            name='dis_date',
            field=models.CharField(default='2023-10-01', max_length=20),
        ),
        migrations.AlterField(
            model_name='patients',
            name='app_date',
            field=models.CharField(default='2023-10-01', max_length=20),
        ),
        migrations.DeleteModel(
            name='sample',
        ),
    ]
