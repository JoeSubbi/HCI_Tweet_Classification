# Generated by Django 3.2.9 on 2021-11-19 00:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_agressive_tweetresults_aggressive'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='UserTweetHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('judgement', models.CharField(choices=[('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Offensive', 'Offensive'), ('Aggressive', 'Aggressive')], default='Neutral', max_length=20)),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
    ]
