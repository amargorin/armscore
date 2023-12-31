# Generated by Django 4.2.3 on 2023-08-01 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0011_alter_membercats_age_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='membercats',
            name='age_category',
            field=models.CharField(choices=[('Мужчины', 'Мужчины'), ('Женщины', 'Женщины'), ('Юниоры 19-21', 'Юниоры 19-21'), ('Юниорки 19-21', 'Юниорки 19-21'), ('Юниоры 16-18', 'Юниоры 16-18'), ('Юниорки 16-18', 'Юниорки 16-18'), ('Юноши 14-15', 'Юноши 14-15'), ('Девушки 14-15', 'Девушки 14-15'), ('Мужчины Мастера 40+', 'Мужчины Мастера 40+'), ('Женщины Мастера 40+', 'Женщины Мастера 40+'), ('Мужчины Гранд мастера 50+', 'Мужчины Гранд мастера 50+'), ('Женщины Гранд мастера 50+', 'Женщины Гранд мастера 50+'), ('Мужчины Сеньор гранд мастера 60+', 'Мужчины Сеньор гранд мастера 60+'), ('Женщины Сеньор гранд мастера 60+', 'Женщины Сеньор гранд мастера 60+')], default='Мужчины', max_length=40),
        ),
        migrations.AlterField(
            model_name='membercats',
            name='group_category',
            field=models.CharField(choices=[('Общая', 'Общая'), ('Любители', 'Любители'), ('Профессионалы', 'Профессионалы'), ('Инвалиды', 'Инвалиды'), ('Инвалиды VIZ', 'Инвалиды VIZ'), ('Инвалиды STAND', 'Инвалиды STAND'), ('Инвалиды HEAR', 'Инвалиды HEAR'), ('Инвалиды SIT', 'Инвалиды SIT')], default='Общая', max_length=40),
        ),
        migrations.AlterField(
            model_name='membercats',
            name='weight_category',
            field=models.CharField(choices=[('55 КГ', '55 КГ'), ('60 КГ', '60 КГ'), ('65 КГ', '65 КГ'), ('70 КГ', '70 КГ'), ('75 КГ', '75 КГ'), ('80 КГ', '80 КГ'), ('85 КГ', '85 КГ'), ('90 КГ', '90 КГ'), ('100 КГ', '100 КГ'), ('110 КГ', '110 КГ'), ('110+ КГ', '110+ КГ')], default='55 КГ', max_length=40),
        ),
    ]
