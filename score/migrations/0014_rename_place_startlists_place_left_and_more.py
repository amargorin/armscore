# Generated by Django 4.2.3 on 2023-08-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0013_remove_membercats_type_match_match_hands'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startlists',
            old_name='place',
            new_name='place_left',
        ),
        migrations.AddField(
            model_name='startlists',
            name='place_right',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]