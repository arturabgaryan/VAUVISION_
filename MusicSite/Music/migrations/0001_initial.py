# Generated by Django 3.1.6 on 2021-02-25 20:32

import Music.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16)),
                ('user', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='DocsRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=500)),
                ('release_name', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('release_date', models.DateField(default=None)),
                ('filthy', models.CharField(max_length=170)),
                ('number', models.CharField(max_length=100)),
                ('cover', models.ImageField(upload_to=Music.models.DocsRequest.get_file_path)),
                ('cover_name', models.CharField(max_length=500)),
                ('release_type', models.CharField(max_length=150)),
                ('artisi_name', models.CharField(default=None, max_length=500)),
                ('vk_style', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='PaspInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default=None, max_length=500)),
                ('who_given', models.CharField(default=None, max_length=500)),
                ('when_given', models.CharField(default=None, max_length=500)),
                ('data_born', models.CharField(default=None, max_length=500)),
                ('place_born', models.CharField(default=None, max_length=500)),
                ('grajdanstvo', models.CharField(default=None, max_length=500)),
                ('artist_name', models.CharField(default=None, max_length=1000)),
                ('seria_num', models.CharField(default=None, max_length=500)),
                ('email', models.CharField(default=None, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=500)),
                ('value', models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default=None, max_length=500)),
                ('name', models.CharField(max_length=250)),
                ('melody_author', models.CharField(max_length=250)),
                ('text_author', models.CharField(max_length=250)),
                ('singer', models.CharField(max_length=250)),
                ('artist', models.CharField(default=None, max_length=250)),
                ('artist_name', models.CharField(default=None, max_length=250)),
                ('release_date', models.DateField(default=None)),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Music.docsrequest')),
            ],
        ),
    ]
