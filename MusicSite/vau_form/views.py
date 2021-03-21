from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from secrets import token_urlsafe
from random import randint


def create_social_or_404(request, name, card):
    try:
        icons = {
            'VK': '/Music/static/media/icons/vk.png',
            'iTunes': '/Music/static/media/icons/itunes.png',
            'Boom': '/Music/static/media/icons/boom.png',
            'Youtube Music': '/Music/static/media/icons/youtube.png',
            'Yandex Music': '/Music/static/media/icons/yandex.png',
            'Spotify': '/Music/static/media/icons/spotify.png',
            'SoundCloud': '/Music/static/media/icons/soundcloud.png',
            'Deezer': '/Music/static/media/icons/deezer.png',
            'AppleMusic': '/Music/static/media/icons/applemusic.png',
        }
        social = Social()
        if 'Собственная' in name:
            social.name = request.POST[f'{name}SecondName']
            social.logo = '/Music/static/media/icons/vauvision-circle.png'
        else:
            social.name = name
            social.logo = icons[name]
        social.link, social.position = request.POST[name], request.POST[f'{name}Position']
        social.card = card
        social.save()
        return
    except KeyError:
        return


def create_network_or_404(request, name, card):
    try:
        icons = {
            'VKontakte': '/Music/static/media/icons/vk.png',
            'instagram': '/Music/static/media/icons/instagram.png',
            'tik tok': '/Music/static/media/icons/tiktok.png',
            'youtube': '/Music/static/media/icons/video_youtube.png'
        }
        social = ArtistNetwork()
        if 'Собственная ' in name:
            social.name = request.POST[f'{name}SecondName']
            social.logo = '/Music/static/media/icons/vauvision-circle.png'
        else:
            social.name = name
            social.logo = icons[name]
        social.link, social.position = request.POST[name], request.POST[f'{name}Position']
        social.card = card
        social.save()
        return
    except KeyError:
        return


def index(request):
    if request.method == 'GET':
        return render(request, 'form-pages/pages/index.html')
    else:

        # Author info
        card = UserCard()
        card.author = request.POST['authorName']
        card.release = request.POST['releaseName']
        token_url = token_urlsafe(randint(4, 7))
        while len(UserCard.objects.filter(url_id=token_url).all()) != 0:
            token_url = token_urlsafe(randint(4, 7))
        card.url_id = token_url
        card.save()

        cover = Cover()
        cover.cover = request.FILES['imageCover']
        cover.card = card
        cover.save()

        create_social_or_404(request, 'VK', card)
        create_social_or_404(request, 'iTunes', card)
        create_social_or_404(request, 'Boom', card)
        create_social_or_404(request, 'Youtube Music', card)
        create_social_or_404(request, 'Yandex Music', card)
        create_social_or_404(request, 'Spotify', card)
        create_social_or_404(request, 'SoundCloud', card)
        create_social_or_404(request, 'Deezer', card)
        create_social_or_404(request, 'AppleMusic', card)
        create_social_or_404(request, 'Собственная ссылка 1', card)
        create_social_or_404(request, 'Собственная ссылка 2', card)
        create_social_or_404(request, 'Собственная ссылка 3', card)

        create_network_or_404(request, 'VKontakte', card)
        create_network_or_404(request, 'instagram', card)
        create_network_or_404(request, 'tik tok', card)
        create_network_or_404(request, 'youtube', card)
        create_network_or_404(request, 'Собственная соц. сеть 1', card)
        create_network_or_404(request, 'Собственная соц. сеть 2', card)
        create_network_or_404(request, 'Собственная соц. сеть 3', card)

        return redirect(f'/{token_url}')



