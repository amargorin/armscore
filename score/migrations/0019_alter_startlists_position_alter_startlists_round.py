# Generated by Django 4.2.3 on 2023-08-04 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0018_startlists_loses_startlists_win_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startlists',
            name='position',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='round',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]