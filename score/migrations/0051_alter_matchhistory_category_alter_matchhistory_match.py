# Generated by Django 4.2.3 on 2023-10-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0050_alter_matchhistory_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchhistory',
            name='category',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='matchhistory',
            name='match',
            field=models.IntegerField(default=0),
        ),
    ]
