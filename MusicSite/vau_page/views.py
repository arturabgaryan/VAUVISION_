from django.shortcuts import render
from vau_form.models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse


def artist_card(request, artistId):
    try:
        card = UserCard.objects.filter(url_id=artistId).get()
        cover = Cover.objects.filter(card=card).get()
        socials = Social.objects.filter(card=card).order_by('position').all()
        networks = ArtistNetwork.objects.filter(card=card).order_by('position').all()
        return render(request, 'user-pages/landing.html', {'card': card, 'cover': cover, 'socials': socials, 'networks': networks})
    except:
        return HttpResponse('<b>Страницы не существует, проверьте правильность ссылки</b>')