# Generated by Django 3.2.14 on 2022-12-12 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_live',
            field=models.CharField(default='false', max_length=25),
        ),
    ]
