# Generated by Django 4.2.3 on 2023-08-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0031_alter_startlists_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startlists',
            name='second_name',
            field=models.CharField(default='', max_length=25),
        ),
    ]
