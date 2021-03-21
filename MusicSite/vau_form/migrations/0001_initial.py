# Generated by Django 3.0.3 on 2020-05-21 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150)),
                ('release', models.CharField(max_length=150)),
                ('url_id', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('AppleMusic', 'Applemusic'), ('iTunes', 'Itunes'), ('Boom', 'Boom'), ('Youtube Music', 'Youtube'), ('Yandex Music', 'Yandex'), ('Spotify', 'Spotify'), ('SoundCloud', 'Soundcloud'), ('Deezer', 'Deezer'), ('VK', 'Vk')], max_length=20)),
                ('link', models.URLField()),
                ('position', models.IntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vau_form.UserCard')),
            ],
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(upload_to='static/media/covers')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vau_form.UserCard')),
            ],
        ),
    ]