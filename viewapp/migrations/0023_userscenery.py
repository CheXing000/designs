# Generated by Django 3.2.16 on 2022-11-24 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewapp', '0022_userways'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserScenery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenery', models.CharField(max_length=85)),
                ('city', models.CharField(max_length=85)),
                ('mark', models.CharField(max_length=85)),
                ('rank', models.CharField(max_length=85)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户收藏景区管理',
                'verbose_name_plural': '用户收藏景区管理',
                'db_table': 'user_scenery',
            },
        ),
    ]
