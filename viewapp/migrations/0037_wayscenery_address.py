# Generated by Django 3.2.16 on 2022-12-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewapp', '0036_sceneryadds'),
    ]

    operations = [
        migrations.AddField(
            model_name='wayscenery',
            name='address',
            field=models.CharField(default='', max_length=85),
            preserve_default=False,
        ),
    ]
