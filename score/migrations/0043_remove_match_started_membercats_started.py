# Generated by Django 4.2.3 on 2023-09-20 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0042_alter_membercats_hands'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='started',
        ),
        migrations.AddField(
            model_name='membercats',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
