from django.db import models


class UserCard(models.Model):
    author = models.CharField(max_length=150)
    release = models.CharField(max_length=150)
    url_id = models.CharField(max_length=250)


class Cover(models.Model):
    cover = models.ImageField(upload_to='Music/static/media/covers/')
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE)


class Social(models.Model):
    name = models.CharField(max_length=20)
    link = models.URLField()
    logo = models.CharField(max_length=100)
    position = models.IntegerField()
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE)


class ArtistNetwork(models.Model):
    name = models.CharField(max_length=20)
    link = models.URLField()
    logo = models.CharField(max_length=100)
    position = models.IntegerField()
    card = models.ForeignKey(UserCard, on_delete=models.CASCADE)