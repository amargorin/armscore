# Generated by Django 4.2.3 on 2023-08-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0010_alter_membercats_age_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membercats',
            name='age_category',
            field=models.CharField(choices=[('Мужчины', 'Man'), ('Женщины', 'Wom'), ('Юниоры 19-21', 'Jm1'), ('Юниорки 19-21', 'Jw1'), ('Юниоры 16-18', 'Jm2'), ('Юниорки 16-18', 'Jw2'), ('Юноши 14-15', 'Jm3'), ('Девушки 14-15', 'Jw3'), ('Мужчины Мастера 40+', 'Mma'), ('Женщины Мастера 40+', 'Wma'), ('Мужчины Гранд мастера 50+', 'Mgm'), ('Женщины Гранд мастера 50+', 'Wgm'), ('Мужчины Сеньор гранд мастера 60+', 'Msg'), ('Женщины Сеньор гранд мастера 60+', 'Wsg')], default='Мужчины', max_length=40),
        ),
        migrations.AlterField(
            model_name='membercats',
            name='group_category',
            field=models.CharField(choices=[('Общая', 'Gen'), ('Любители', 'New'), ('Профессионалы', 'Pro'), ('Инвалиды', 'Inv'), ('Инвалиды VIZ', 'Viz'), ('Инвалиды STAND', 'Sta'), ('Инвалиты HEAR', 'Hea'), ('Инвалиды SIT', 'Sit')], default='Общая', max_length=40),
        ),
        migrations.AlterField(
            model_name='membercats',
            name='weight_category',
            field=models.CharField(choices=[('55 КГ', 'C55'), ('60 КГ', 'C60'), ('65 КГ', 'C65'), ('70 КГ', 'C70'), ('75 КГ', 'C75'), ('80 КГ', 'C80'), ('85 КГ', 'C85'), ('90 КГ', 'C90'), ('100 КГ', 'C10'), ('110 КГ', 'C11'), ('110+ КГ', 'C12')], default='55 КГ', max_length=40),
        ),
    ]