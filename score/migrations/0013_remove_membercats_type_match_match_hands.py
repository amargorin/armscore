# Generated by Django 4.2.3 on 2023-08-02 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0012_match_current_alter_membercats_age_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membercats',
            name='type_match',
        ),
        migrations.AddField(
            model_name='match',
            name='hands',
            field=models.CharField(choices=[('0', 'Обе руки'), ('1', 'Правая'), ('2', 'Левая')], default='0', max_length=1),
        ),
    ]