# Generated by Django 3.1.7 on 2021-03-25 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='change',
            field=models.BooleanField(default=False),
        ),
    ]
