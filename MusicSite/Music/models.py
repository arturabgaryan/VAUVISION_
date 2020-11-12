from django.db import models
from django.contrib.auth.models import User
import os

paths = os.path.abspath('')

class AuthCodes(models.Model):
    code = models.CharField(max_length=16)
    user = models.EmailField()


class Counter(models.Model):
    number = models.CharField(max_length=150)


class DocsRequest(models.Model):
    contact = models.CharField(max_length=500)
    release_name = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.EmailField()
    release_date = models.DateField(default=None)
    filthy = models.CharField(max_length=170)
    number = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='Music/static/images/covers')
    release_type = models.CharField(max_length=150)
    vk_style = models.CharField(max_length=5)


class Track(models.Model):
    full_name = models.CharField(max_length=500,default=None)
    name = models.CharField(max_length=250)
    melody_author = models.CharField(max_length=250)
    text_author = models.CharField(max_length=250)
    singer = models.CharField(max_length=250)
    request = models.ForeignKey(DocsRequest, on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=250,default=None)
    artist_name = models.CharField(max_length=250,default=None)


class Scan(models.Model):
    photo = models.ImageField(upload_to='Music/static/images/scans')
    photo_url = models.CharField(max_length=500,default=None)
    request = models.ForeignKey(DocsRequest, on_delete=models.CASCADE)


class PaspInfo(models.Model):
    full_name = models.CharField(max_length=500,default=None)
    who_given = models.CharField(max_length=500,default=None)
    when_given = models.CharField(max_length=500,default=None)
    data_born = models.CharField(max_length=500,default=None)
    place_born = models.CharField(max_length=500,default=None)
    email = models.CharField(max_length=500,default=None)




