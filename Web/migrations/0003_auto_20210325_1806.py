# Generated by Django 3.1.7 on 2021-03-25 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_persona_change'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='change',
        ),
        migrations.AddField(
            model_name='usuario',
            name='change',
            field=models.BooleanField(default=False),
        ),
    ]