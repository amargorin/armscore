# Generated by Django 4.2.3 on 2023-08-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0007_alter_membercats_age_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='membercats',
            name='match_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
