from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from Music.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import smtplib
import os
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
import yadisk
import io
from datetime import datetime
from typing import Type
import random
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from .models import Counter
from django.http import JsonResponse
from django.conf import settings
import subprocess


class PathExistsError:
    pass


def enter(request):
    return render(request, 'unauthmain.html')


def upload(request):
    APP_TOKEN = 'AgAAAAA_8uwPAAarbHv2-khOnkCRmzitHRkTKdU'
    y = yadisk.YaDisk(token=APP_TOKEN)
    name = request.GET.get('id',None)
    folder_path = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{name}"
    files = request.FILES[name]
    try:
        y.upload(path_or_file=io.BytesIO(request.FILES[name].read()),
                 dst_path=f'{folder_path}/dogovor.pdf')

    except:
        pass
    y.download(f"{folder_path}/dogovor.pdf", f"Music/static/documents/{name}_offer.pdf")
    return redirect('/account')


def authorization(request):
    return render(request, 'authorization.html')


def registration(request):
    return render(request, 'registration.html')


def main(request):
    return render(request,'main.html')


def account(request):
    tracks = Track.objects.filter(artist=request.user.username)
    return render(request,'accountpage.html',{'task':tracks,'name':request.user.username})


def change_profile_info_page(request):
    return render(request,'change_profile.html',{'email':request.user.email,'name':request.user.username})


def generate_pass():
    alphabet = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    password = ''
    for i in range(15):
        password += random.choice(alphabet)
    return password


def change(request):
    name = request.GET.get('usrnm', None)
    passw = request.GET.get('psw', None)
    passw2 = request.GET.get('psw2', None)
    passw_old = request.GET.get('psw_old',None)
    user = User.objects.get(username=name)
    if passw and passw2:
        if passw == passw2:
            if (user == request.user) and (check_password(passw_old, user.password)):
                print(3)
                user.set_password(passw)
                user.save()
                return redirect('/account')
    else:
        redirect('/change_profile_info_page')


def create(request):
    name = request.GET.get('log', None)
    email = request.GET.get('email', None)
    passw = request.GET.get('pwd', None)
    passw2 = request.GET.get('pwd2',None)
    if email and passw and passw2:
        if passw2 != passw:
            messages.info(request, "Пароли не совпадают")
            return redirect('/reg_page')
        if User.objects.get(password=passw):
            messages.info(request, "Такой пароль уже существует")
            return redirect('/reg_page')
        else:
            user = User.objects.create_user(username=name, email=email, password=passw)
            user.save()

        return redirect('/')


def log_in(request):
    log = request.GET.get('usrnm', None)
    pwd = request.GET.get('psw', None)
    if log and pwd:
        user = authenticate(request, username=log, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            print('Пароль не верный')
            return redirect('/authorization')


def send_email(request):
    addr_from = "ar12.abgaryan@gmail.com"                         # Отправитель
    password  = "Artur8043"
    addr_to = request.GET.get('email', None)
    name = request.GET.get('name', None)

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From'] = addr_from                              # Адресат
    msg['To'] = addr_to                                # Получатель
    msg['Subject'] = "Вы включены в рассылку VAUVISION"                               # Тема сообщения

    body = name + ", вас будут оповещать о всех событиях через рассылку. Оставайтесь на связи!)"
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        return redirect('/')


def form(request):
    return render(request,'index.html')


def index(request):
    APP_TOKEN = 'AgAAAAA_8uwPAAarbHv2-khOnkCRmzitHRkTKdU'
    y = yadisk.YaDisk(token=APP_TOKEN)

    releaseType = request.POST['releaseType']
    releaseName = request.POST['releaseName']
    if request.POST['filthyCheck'] == 'false':
        filthyTracks = 'без мата'
    else:
        filthyTracks = request.POST['filthyTracks']
    releaseDate = request.POST['releaseDate']
    releasePlaces = request.POST['releasePlaces']
    releaseSubInfo = request.POST['releaseSubInfo']
    if request.POST['videoCheck'] == 'true':
        track_url = request.POST['clips']
    else:
        track_url = 'нет клипов'
    info_songs = {}
    for e in request.POST:
        if ('.wav' in e) or ('.mp3' in e):
            name = e.split('__')[0]
            field = e.split('__')[1]
            if name not in info_songs:
                info_songs[name] = {}
            info_songs[name][field] = request.POST[e]
    name = f'{releaseName.replace(" ", "__")}'
    email = request.POST['email']

    try:
        artist_name = releaseName.split('-')[0]
    except:
        artist_name = ''

    try:
        user = User.objects.get(username=email)

    except:
        user = None

    if user is None:
        generated_pass = generate_pass()
        user = User.objects.create_user(username=email, email=email, password=generated_pass)
        user.save()

        addr_from = "ar12.abgaryan@gmail.com"  # Отправитель
        password = "Artur8043"
        addr_to = email

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = "Аккаунт VAUVISION успешно создан!"  # Тема сообщения

        body = artist_name + ", информация о зарегестрированном треке будет в вашем личном кабинете \n Логин: {} \n Пароль: {}".format(
            email, generated_pass)  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(addr_from, password)
        server.send_message(msg)
        server.quit()


    if name not in [directory.name for directory in list(y.listdir('/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/'))]:
        new_request = DocsRequest()
        new_request.contact = request.POST['vk']
        new_request.release_name = releaseName
        new_request.email = email
        new_request.vk_style = request.POST['vkDecor']
        new_request.release_date = releaseDate
        new_request.filthy = filthyTracks
        new_request.release_type = releaseType
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)

        if len(day) == 1:
            day = f'0{day}'
        if len(month) == 1:
            month = f'0{month}'

        number = f'{day}{month}{year}'
        new_request.number = number
        new_request.cover = request.FILES["releaseCover"]
        cover_format = new_request.cover.name.split(".")[-1]
        new_request.cover.name = f'cover__{new_request.email}.{cover_format}'

        new_request.save()
        try:
            textsFiles = request.FILES['musicTexts']
        except:
            textsFiles = None
        try:
            tiktok = request.POST['tiktokTime']
        except:
            tiktok = 'Не указано'

        try:
            genre = request.POST['releaseGenre']
        except:
            genre = 'Не указан'

        info_to_file = f"1) Краткая информация о релизе: \n\nВК автора {request.POST['vk']}\nПочта автора: {email}\nОформление карточни в ВК: {request.POST['vkDecor']}\nТип релиза: {releaseType}\nИмя релиза: {releaseName}\nТреки с матом: {filthyTracks}\nДата релиза: {releaseDate}\nПлощадки релиза: {releasePlaces}\nВоспроизводить трек в Tik Tok с {tiktok}c.\nЖанр: {genre}\nДоп. информация: {releaseSubInfo}\nПользователь узнал о лейбле: {request.POST['infoSource']}\nСсылка на клипы: {track_url}\n2) Треки:\n\n"
        for track in info_songs:
            new_track = Track()
            new_track.name = str(track).replace('.wav', '').replace('.mp3', '')
            new_track.melody_author = info_songs[track]["melodyAuthor"]
            new_track.text_author = info_songs[track]["textAuthor"]
            new_track.singer = info_songs[track]["artist"]
            new_track.request = new_request
            new_track.artist = email
            new_track.artist_name = artist_name
            new_track.full_name = f'{releaseName.replace(" ", "__")}'
            new_track.save()

            info_to_file += f'Имя: {track}\nАвтор мелодии: {info_songs[track]["melodyAuthor"]}\nАвтор текста: {info_songs[track]["textAuthor"]}\nИсполнитель: {info_songs[track]["artist"]}\n\n'

        name = f'{releaseName.replace(" ", "__")}'
        folder_path = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{name}"

        y.mkdir(folder_path)
        for track in request.FILES.getlist('tracks'):
            y.upload(path_or_file=io.BytesIO(track.read()), dst_path=f'{folder_path}/{track}')
        y.upload(path_or_file=io.BytesIO(request.FILES.get('releaseCover').read()),
                 dst_path=f'{folder_path}/cover.jpeg')
        page = 1

        if textsFiles != None:
            y.upload(path_or_file=io.BytesIO(textsFiles.read()), dst_path=f'{folder_path}/texts.docx')

        for scan in request.FILES.getlist('scans'):
            y.upload(path_or_file=io.BytesIO(scan.read()), dst_path=f'{folder_path}/passport_scan_{page}')

            new_scan = Scan()
            new_scan.photo = scan
            new_scan.photo.name = f'scan__{new_request.email}__{page}.{new_scan.photo.name.split(".")[-1]}'
            new_scan.request = new_request
            new_scan.photo_url = new_scan.photo.name.split('/')[-1]
            new_scan.save()
            page += 1
        y.upload(path_or_file=io.BytesIO(info_to_file.encode('utf-8')), dst_path=f'{folder_path}/brief.txt')


    return redirect('https://vk.com/vauvisionlabel/')


def panel(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            scan_requests = DocsRequest.objects.all()
            return render(request, 'admin-panel/pages/admin.html', {'scan_requests': scan_requests})
        else:
            return redirect('/form-admin/login')
    else:
        return redirect('/form-admin/login')


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def admin_login(request):
        if request.method == 'GET':
            return render(request, 'admin-panel/pages/login_page.html')
        else:
            pwd = request.POST['password']
            username = request.POST['username']
            user = authenticate(username=username, password=pwd)
            if user.is_superuser:
                login(request, user)
                return redirect('/form-admin')
            else:
                return render(request, 'admin-panel/pages/login_page.html', {'login_error': 'Пользователя не существует'})


def generate_auth_code(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            email = request.POST['email']
            if len(AuthCodes.objects.filter(user=email).all()) == 0:
                chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                code = ''
                for _ in range(16):
                    code += random.choice(chars)
                link = AuthCodes()
                link.user = email
                link.code = code
                link.save()
                return render(request, 'admin-panel/pages/admin.html', {'result': f'Код для регистрации: {code}'})
            else:
                return render(request, 'admin-panel/pages/admin.html',
                              {'result': 'Код для этого пользователя уже зарегестрирован'})


def admin_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        access_code = request.POST['access-code']
        user = authenticate(username=username, password=password, email=email)
        if not user:
            if len(AuthCodes.objects.filter(code=access_code, user=email).all()) != 0:
                new_user = User.objects.create_superuser(username=username, email=email, password=password)
                new_user.save()
                login(request, new_user)
                AuthCodes.objects.filter(code=access_code, user=email).get().delete()
                return redirect('/form-admin')
            else:
                return render(request, 'admin-panel/pages/login_page.html', {'signup_error': 'Код регистрации недействительный, обратитесь к администратору'})
        else:
            return render(request, 'admin-panel/pages/login_page.html',
                          {'signup_error': 'Пользователь уже существует, пожалуйста ВОЙДИТЕ в аккаунт'})

    else:
        return redirect('/form-admin/login/')


def change_name(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            name, id = request.GET['name'], request.GET['id']
            print(name)
            track = Track.objects.get(pk=id)
            track.name = name
            track.save()
            return JsonResponse({'content': 'ok'})
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')


def submit_request(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            months = {
                1: 'января',
                2: 'февраля',
                3: 'марта',
                4: 'апрель',
                5: 'мая',
                6: 'июня',
                7: 'июля',
                8: 'августа',
                9: 'сентября',
                10: 'октября',
                11: 'ноября',
                12: 'декабря',

            }
            if request.method == 'GET':
                request_id = request.GET['id']
                current_request = DocsRequest.objects.get(pk=request_id)
                scans = Scan.objects.filter(request=current_request).all()
                for scan in scans:
                    scan.photo_url = scan.photo.name.split('/')[-1]
                tracks = Track.objects.filter(request=current_request).all()
                return render(request, 'admin-panel/pages/submit.html',
                              {'request': current_request, 'scans': scans, 'tracks': tracks})
            else:
                APP_TOKEN = 'AgAAAAA_8uwPAAarbHv2-khOnkCRmzitHRkTKdU'
                y = yadisk.YaDisk(token=APP_TOKEN)
                doc = DocxTemplate("Music/static/documents/template.docx")
                request_id = request.GET['id']
                sum_request = DocsRequest.objects.get(pk=request_id)
                count = len(Counter.objects.filter(number=sum_request.number)) + 1
                context = {
                    'NAME': request.POST['NAME'],
                    'FULL_NAME': request.POST['FULLNAME'],
                    'EMAIL': request.POST['EMAIL'],
                    'COUNTRY': request.POST['COUNTRY'],
                    'BIRTH_DATE': request.POST['BIRTH_DATE'],
                    'NUMBER': f'{sum_request.number}-{count}',
                    'INITIALS': request.POST['INITIALS'],
                    'BIRTH_PLACE': request.POST['BIRTH_PLACE'],
                    'PASSPORT_SERIE': request.POST['PASSPORT_SERIE'],
                    'PASSPORT_NUMBER': request.POST['PASSPORT_NUMBER'],
                    'GIVEN_BY': request.POST['GIVEN_BY'],
                    'GIVEN_DATE': request.POST['GIVEN_DATE'],
                    'REGISTRATION': request.POST['REGISTRATION'],
                    'VK': sum_request.contact,
                    'MONTH': f'{months[datetime.now().month]} ',
                    'IMAGE': InlineImage(doc, image_descriptor=f'{sum_request.cover}', width=Mm(100)),
                    "DAY": datetime.now().day,
                    'YEAR': datetime.now().year,
                    'TRACKS': Track.objects.filter(request=sum_request).all()
                }
                name = sum_request.release_name
                folder_path = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{name.replace(' ', '__')}"
                offer_name = f'offer__vauvision__{context["NUMBER"]}'
                try:
                    doc.render(context)
                except:
                    context['IMAGE'] = 'Вставьте обложку релиза'
                doc.save(f"Music/static/documents/{offer_name}.docx")
                path = '{}/Music/static/documents/{}.docx'.format(str(os.path.abspath('')),offer_name)
                filepath = '{}/Music/static/documents/{}.pdf'.format(str(os.path.abspath('')),offer_name)
                output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf', path])
                os.rename('{}/{}.pdf'.format(str(os.path.abspath('')),offer_name), '{}/Music/static/documents/{}.pdf'.format(str(os.path.abspath('')),offer_name))
                y.upload(path_or_file=f"Music/static/documents/{offer_name}.pdf",
                         dst_path=f'{folder_path}/{offer_name}.pdf/')

                addr_from = "ar12.abgaryan@gmail.com"  # Отправитель
                password = "Artur8043"
                addr_to = request.POST['EMAIL']

                msg = MIMEMultipart()  # Создаем сообщение
                msg['From'] = addr_from  # Адресат
                msg['To'] = addr_to  # Получатель
                msg['Subject'] = "Аккаунт VAUVISION успешно создан!"  # Тема сообщения

                body = "{}, договор о недавно зарегестрированном треке прикреплен ниже".format(
                    request.POST['FULLNAME'])  # Текст сообщения
                msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

                ctype, encoding = mimetypes.guess_type(filepath)
                maintype, subtype = ctype.split('/', 1)
                with open(filepath, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                    file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                    fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
                file.add_header('Content-Disposition', 'attachment', filename=offer_name)  # Добавляем заголовки
                msg.attach(file)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(addr_from, password)
                server.send_message(msg)
                server.quit()

                current_request = DocsRequest.objects.filter(id=request_id).delete()
                Scan.objects.filter(request=current_request).delete()
                #os.rename(f'{offer_name}.pdf', f'static/documents/{offer_name}.pdf')
                counter = Counter()
                counter.number = sum_request.number
                counter.save()

                return redirect('/form-admin')
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')


def delete_request(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'GET':
                request_id = request.GET['id']
                current_request = DocsRequest.objects.filter(id=request_id).get()
                Scan.objects.filter(request=current_request).delete()
                Track.objects.filter(request=current_request).delete()
                current_request.delete()
            return redirect('/form-admin')
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')
