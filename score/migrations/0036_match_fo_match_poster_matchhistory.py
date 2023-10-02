# Generated by Django 4.2.3 on 2023-09-12 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0035_match_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='fo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='poster',
            field=models.ImageField(default='default_poster.png', upload_to=''),
        ),
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_name', models.CharField(max_length=25)),
                ('win_surname', models.CharField(max_length=25)),
                ('win_second_name', models.CharField(default='', max_length=25)),
                ('los_name', models.CharField(max_length=25)),
                ('los_surname', models.CharField(max_length=25)),
                ('los_second_name', models.CharField(default='', max_length=25)),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='score.membercats')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.match')),
            ],
        ),
    ]
