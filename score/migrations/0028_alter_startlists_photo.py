# Generated by Django 4.2.3 on 2023-08-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0027_alter_startlists_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startlists',
            name='photo',
            field=models.ImageField(default='static/images/Man.png', upload_to='media'),
        ),
    ]
