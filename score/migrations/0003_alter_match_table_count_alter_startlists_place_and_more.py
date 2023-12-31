# Generated by Django 4.2.3 on 2023-07-12 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_match_table_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='table_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='place',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='round',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startlists',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
