# Generated by Django 2.1.5 on 2020-10-27 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0011_auto_20201027_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='photo_url',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
