# Generated by Django 3.1.6 on 2021-02-22 09:50

import Music.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='docsrequest',
            name='cover_name',
            field=models.CharField(default='default', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='docsrequest',
            name='cover',
            field=models.ImageField(upload_to=Music.models.DocsRequest.get_file_path),
        ),
    ]