# Generated by Django 4.2.1 on 2023-09-08 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HospitalManagement', '0004_rename_contact_us_contact_us_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='admins',
            fields=[
                ('admin_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
