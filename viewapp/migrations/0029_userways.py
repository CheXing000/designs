# Generated by Django 3.2.16 on 2022-11-24 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewapp', '0028_delete_userways'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenerys', models.CharField(max_length=85)),
                ('start_time', models.CharField(max_length=85)),
                ('end_time', models.CharField(max_length=85)),
                ('days', models.CharField(max_length=45)),
                ('say_people', models.IntegerField()),
                ('is_on', models.CharField(max_length=45)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户路线管理',
                'verbose_name_plural': '用户路线管理',
                'db_table': 'user_way_detail',
            },
        ),
    ]
