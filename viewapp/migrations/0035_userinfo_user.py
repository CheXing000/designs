# Generated by Django 3.2.16 on 2022-12-09 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewapp', '0034_userinfo_usersafe'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='user',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
