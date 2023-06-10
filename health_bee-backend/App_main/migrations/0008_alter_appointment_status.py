# Generated by Django 4.2.1 on 2023-05-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0007_testresult_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Requested', 'Requested'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Missed', 'Missed')], max_length=20),
        ),
    ]