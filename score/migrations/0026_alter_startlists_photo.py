# Generated by Django 4.2.3 on 2023-08-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0025_startlists_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startlists',
            name='photo',
            field=models.ImageField(default='', upload_to='static/images'),
        ),
    ]
