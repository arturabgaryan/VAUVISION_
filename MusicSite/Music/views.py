from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Music.models import AuthCodes, Counter, DocsRequest, Track, PaspInfo, \
    PromoCodes,Requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import smtplib
import os
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yadisk
import io
from datetime import datetime
import random
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from django.http import JsonResponse
import subprocess
import time
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.core import exceptions
import uuid
from yookassa import Configuration, Payment
from django.template.loader import render_to_string


class PathExistsError:
    pass


def send_email_util(
    addr_from: str, password: str, addr_to: str, subject: str, body: str
) -> 1:
    """Sending mail to specified address"""

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    return 1


@csrf_exempt
def test(request):
    context = {}
    context.update(csrf(request))
    context['user'] = request.user
    if request.user.is_authenticated:
        return render(request, 'test..html', context)
    else:
        return render(request, 'test..html', context)


def enter(request):
    return render(request, 'unauthmain.html')


def back(request):
    return redirect('/account')


@ensure_csrf_cookie
def upload(request):
    APP_TOKEN = 'AgAAAAA_8uwPAAarbHv2-khOnkCRmzitHRkTKdU'
    y = yadisk.YaDisk(token=APP_TOKEN)
    name = request.GET.get('id', None)
    name = name[:-2]
    name2 = name + "_name"

    folder_path = f"/КАТАЛОГ VAUVISION/{name + '(1)'}"
    folder_path2 = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{name + '(1)'}"
    _ = request.FILES.get(name+"_name")
    try:
        y.upload(
            path_or_file=io.BytesIO(request.FILES.get(name2)),
            dst_path=f"{folder_path}/Signed-{name}.pdf",
            overwrite=True
        )
    except:
        y.upload(
            path_or_file=io.BytesIO(
                request.FILES.get(name2)),
            dst_path=f"{folder_path2}/Signed-{name}.pdf",
            overwrite=True
        )

    try:
        y.download(
            f"{folder_path}/Signed-{name}.pdf",
            f"Music/static/documents/Signed-{name.replace(' ','_')}_offer.pdf"
        )
    except:
        y.download(
            f"{folder_path2}/Signed-{name}.pdf",
            f"Music/static/documents/Signed-{name}_offer.pdf"
        )


    return redirect('/account')


def authorization(request):
    return render(request, 'authorization.html')


def registration(request):
    return render(request, 'registration.html')


def main(request):
    return render(request, 'main.html')


def account(request):
    if request.user.is_authenticated:
        path = '{}/Music/static/documents/Signed-)(_offer.pdf'.format(
            str(os.path.abspath('')))
        tracks = Requests.objects.filter(artist=request.user.username)
        signed_tracks = []
        for track in tracks:
            if os.path.isfile(path.replace(')(',track.artist_name.replace(' ','_') + '_-_' + track.full_name.replace(' ','_'))):
                signed_tracks.append(track.full_name)
                print("Yes:", track.full_name)
            else:
                print('No')
        return render(request, 'accountpage.html', {
            'task': tracks,
            'name': request.user.username,
            'signed_tracks': signed_tracks
        })
    else:
        return render(request, 'authorization.html')


def change_profile_info_page(request):
    return render(request, 'change_profile.html', {
        'email': request.user.email, 'name': request.user.username})


def generate_pass():
    alphabet = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    password = ''
    for i in range(15):
        password += random.choice(alphabet)
    return password


def change(request):
    name = request.POST.get('usrnm', None)
    passw = request.POST.get('psw', None).replace(' ', '')
    passw2 = request.POST.get('psw2', None).replace(' ', '')
    passw_old = request.POST.get('psw_old', None).replace(' ', '')

    try:
        user = User.objects.get(username=name)
    except exceptions.ObjectDoesNotExist:
        user = None

    if passw and passw2:
        if passw == passw2:
            if (user == request.user) and (
                check_password(passw_old, user.password)
            ):
                user.set_password(passw)
                user.save()
                user = authenticate(request, username=name, password=passw)
                if user is not None:
                    login(request, user)
                return redirect('/account')
            else:
                return render(request, 'change_profile.html', {
                    'error': 'Данные введены не верно'})
        else:
            return render(request, 'change_profile.html', {
                'error': 'Пароли не совпадают'})
    else:
        return render(request, 'change_profile.html', {
            'error': 'Заполните все поля'})


def create(request):
    name = request.GET.get('log', None)
    email = request.GET.get('email', None)
    passw = request.GET.get('pwd', None).replace(' ', '')
    passw2 = request.GET.get('pwd2', None).replace(' ', '')
    if email and passw and passw2:
        if passw2 != passw:
            messages.info(request, "Пароли не совпадают")
            return redirect('/reg_page')
        if User.objects.get(password=passw):
            messages.info(request, "Такой пароль уже существует")
            return redirect('/reg_page')
        else:
            user = User.objects.create_user(
                username=name, email=email, password=passw)
            user.save()

        return redirect('/')


def log_in(request):
    log = request.POST.get('usrnm', None)
    pwd = request.POST.get('psw', None).replace(' ', '')
    if log and pwd:
        user = authenticate(request, username=log, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            return render(request, 'authorization.html', {
                'error': 'Пароль не верный'})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def send_email(request):
    time.ctime()
    time_list = time.localtime()
    _ = time_list[3]  # hours var
    # print(hours)
    # if 5 <= int(hours) <= 12:
    #     daytime = 'Доброго утра, '
    # elif 12 <= int(hours) <= 18:
    #     daytime = 'Доброго дня, '
    # elif 18 <= int(hours) <= 22:
    #     daytime = 'Доброго вечера, '
    # else:
    #     daytime = 'Доброй ночи, '
    addr_from = "vau@vauvision.com"                         # Отправитель
    password = "20052005Vauvision!"
    addr_to = request.GET.get('email', None)
    name = request.GET.get('name', None)

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From'] = addr_from                              # Адресат
    msg['To'] = addr_to                                # Получатель
    msg['Subject'] = "Вы включены в рассылку VAUVISION"  # Тема сообщения

    body = 'Добрый день, ' + name + \
        ", вас будут оповещать о всех событиях через рассылку. Оставайтесь на связи!)"
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    if request.user.is_authenticated:
        return redirect('/main')
    else:
        return redirect('/')


def form(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
    return render(request, 'index.html')


@csrf_exempt
def index(request):
    print("request files: \n", request.FILES)
    print("request post\n", request.POST)
    print("request files list tracks:\n", request.FILES.getlist('files'))

    email = request.POST.get('email', None)
    # filess = request.FILES.get('file1',None)

    try:
        user = User.objects.get(username=email)
    except exceptions.ObjectDoesNotExist:
        generated_pass = generate_pass()
        user = User.objects.create_user(
            username=email, email=email, password=generated_pass)
        user.save()

        if send_email_util(
                addr_from="vau@vauvision.com",
                password="20052005Vauvision!",
                addr_to=email,
                subject="Аккаунт VAUVISION успешно создан!",
                body="""Добрый день!
        Вы отправили заявку на дистрибуцию на лейбле VAUVISION.\n
        Теперь у вас на сайте есть личный кабинет, где вы можете видеть свои загруженные релизы, договоры, получить отчёты о прослушиваниях и прочую информацию. Функционал кабинета постепенно будет пополняться.\n\n
        Логин: {} \nПароль: {} \n\n
        Пожалуйста, сохраните логин и пароль от личного кабинета. Скоро на почту придет письмо с договором и дальнейшие инструкции.\n
        По всем возникающим вопросам пишите в сообщения паблика https://vk.com/vauvisionlabel, либо в телеграмм https://teleg.run/vauvision_bot""".format(
                    email, generated_pass)
        ) != 0:
            print("EMAIL WAS SENT")

    APP_TOKEN = 'AgAAAAAVXvrzAAZUx8r6G2rp3EZGpwXtTZI4KNg'
    y = yadisk.YaDisk(token=APP_TOKEN)

    name = request.POST.get('releaseName', None)

    art_name = request.POST.get('artistName', None)
    folder_name = art_name + ' - ' + name + '(1)'
    try:
        paspinfo = PaspInfo.objects.get(email=email)
    except:
        paspinfo = PaspInfo.objects.create(
            full_name=request.POST.get('FULLNAME', None),
            who_given=request.POST.get('GIVEN_BY', None),
            when_given=request.POST.get('GIVEN_DATE', None),
            data_born=request.POST.get('BIRTH_DATE', None),
            place_born=request.POST.get('REGISTRATION', None),
            grajdanstvo=request.POST.get('COUNTRY', None),
            seria_num=request.POST.get('SERIE_NUM', None),
            artist_name=request.POST.get('artistName', None),
            email=email
        )
        paspinfo.save()

    for i in range(1000):
        if folder_name in [directory.name for directory in list(
            y.listdir('/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/')
        )]:
            folder_name = folder_name[:-2] + str(i) + ')'
        else:
            break


    if request.POST.get('filthyCheck', None) == 'Да':
        filthy = request.POST.get('filthyTracks', None)
    else:
        filthy = 'Нет'

    docsrequest = DocsRequest.objects.create(
        contact=request.POST.get('vk', None),
        release_name=name,
        email=email,
        release_date=datetime.strptime(
            request.POST.get('releaseDate', None), "%Y-%m-%d"),
        filthy=filthy,
        release_type=request.POST.get('releaseType', None),
        number=datetime.now().strftime("%d%m%Y"),
        cover=request.FILES.get('releaseCover', None),
        artisi_name=request.POST.get('artistName', None),
        cover_name='cover__{}.{}'.format(
            email,
            request.FILES.get('releaseCover', None).name.split(".")[-1]),
    )
    docsrequest.save()
    req = Requests.objects.create(
        artist_name=request.POST.get('artistName', None),
        artist=email,
        name=request.POST.get('releaseName', None),
        full_name=request.POST.get('releaseName', None),
        release_date=datetime.strptime(
            request.POST.get('releaseDate', None), "%Y-%m-%d"),
    )
    req.save()

    tiktok = request.POST.get('tiktokTime', None)
    genre = request.POST.get('releaseGenre', 'Не указан')

    info_to_file = f"""1) Краткая информация о релизе: \n
    ВК автора {docsrequest.contact}
    Spotify:{request.POST.get('spotify', None)}
    Карточка AppleMusic:{request.POST.get('appmusic', None)}
    Почта автора: {email}
    ----------------------------------------------------------------
    Оформление карточни в ВК: Тип релиза: {docsrequest.release_type}
    Имя релиза: {docsrequest.release_name}
    Имя артиста: {request.POST.get('artistName', None)}
    Треки с матом: {docsrequest.filthy}
    Дата релиза: {docsrequest.release_date}
    Площадки релиза: {request.POST.get('releasePlaces', None)}
    Воспроизводить трек в Tik Tok с {tiktok}c.
    Жанр: {genre}
    Доп. информация: {request.POST.get('releaseSubInfo', None)}
    Промо-план: {request.POST.get('promo-plan', None)}
    Пользователь узнал о лейбле: {request.POST.get('infoSource', None)}
    ----------------------------------------------------------------"""

    files = [key for key, value in request.POST.items() if 'text' in key]
    files = [i.split("_")[0] for i in files]

    info_to_file = ""
    for f in files:
        track = Track.objects.create(
            name=".".join(f.split(".")[:-1]),
            melody_author=request.POST.get(str(f) + '_music', None),
            text_author=request.POST.get(str(f) + '_text', None),
            singer=request.POST.get(str(f) + '_artis', None),
            request=docsrequest,
            artist=email,
            artist_name=request.POST.get('artistName', None),
            full_name=request.POST.get('releaseName', None),
            release_date=datetime.strptime(
                request.POST.get('releaseDate', None), "%Y-%m-%d")
        )
        track.save()

        info_to_file += f"""\nИмя: {f}
    Автор мелодии: {track.melody_author}
    Автор текста: {track.text_author}
    Исполнитель: {track.singer}\n\n"""

    folder_path = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{folder_name}"

    y.mkdir(folder_path)
    for track in request.FILES.getlist('files'):
        y.upload(
            path_or_file=io.BytesIO(track.read()),
            dst_path=f'{folder_path}/{track}')

    y.upload(
        path_or_file=io.BytesIO(request.FILES.get('releaseCover').read()),
        dst_path=f'{folder_path}/cover.jpeg')

    # for file in filess:
    #     y.upload(
    #         path_or_file=io.BytesIO(file),
    #         dst_path=f'{folder_path}/cover.jpeg')

    textsFiles = request.FILES.get('musicTexts', None)
    if textsFiles is not None:
        y.upload(
            path_or_file=io.BytesIO(textsFiles.read()),
            dst_path=f'{folder_path}/texts.docx')

    appFiles = request.FILES.get('CaraoceMusicTexts', None)
    if appFiles is not None:
        y.upload(
            path_or_file=io.BytesIO(appFiles.read()),
            dst_path=f'{folder_path}/texts.ttml')

    info_to_file = render_to_string('breif.txt', {
        'docsrequest_contact': docsrequest.contact,
        'spotify': request.POST.get('spotify', 'Нет'),
        'applemusic': request.POST.get('appmusic', 'Нет'),
        'email': email,
        'artist_name': request.POST.get('artistName', None),
        'docsrequest_release_type': docsrequest.release_type,
        'docsrequest_release_name': docsrequest.release_name,
        'docsrequest_filthy': docsrequest.filthy,
        'docsrequest_release_date': docsrequest.release_date,
        'releasePlaces': request.POST.get('releasePlaces', 'Нет данных'),
        'tiktok': tiktok,
        'genre': genre,
        'releaseSubInfo': request.POST.get('releaseSubInfo', 'Нет данных'),
        'promo_plan': request.POST.get('promo-plan', 'Нет данных'),
        'infoSource': request.POST.get('infoSource', 'Нет данных'),
        'f': f,
        'tracks': info_to_file,
        'paspinfo_full_name': paspinfo.full_name,
        'paspinfo_when_given': paspinfo.when_given,
        'paspinfo_who_given': paspinfo.who_given,
        'paspinfo_data_born': paspinfo.data_born,
        'paspinfo_place_born': paspinfo.place_born,
        'COUNTRY': request.POST.get('COUNTRY', 'Нет данных'),
        'SERIE_NUM': request.POST.get('SERIE_NUM', 'Нет данных'),
    })
    y.upload(path_or_file=io.BytesIO(
        info_to_file.encode('utf-8')),
        dst_path=f'{folder_path}/brief.txt')

    cost = request.POST.get('cost', 0)
    code = request.POST.get('code', None)

    code_val = 0
    try:
        PromoCode = PromoCodes.objects.get(name=code)
        code_val = PromoCode.value
    except:
        pass
    print(code_val)
    if code_val != 0:
        cost = int(cost) - int(code_val)
    else:
        pass
    Configuration.account_id = 777380
    Configuration.secret_key = 'live_LVF05e4VifbQannin4i6BakLHjkECd1YpIlkR2SsOTI'

    payment = Payment.create({
        "amount": {
            "value": str(cost),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://vk.com/vauvisionlabel/"
        },
        "capture": True,
        "description": "Заказ {} - {}".format(request.POST.get('releaseName', None).replace(
            " ", "__"), request.POST.get('artistName', None))
    }, uuid.uuid4())

    confirmation_url = payment.confirmation.confirmation_url

    return redirect(confirmation_url)


def panel(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            scan_requests = DocsRequest.objects.all().order_by('-create_time')
            promocodes = PromoCodes.objects.all()
            return render(request, 'admin-panel/pages/admin.html', {
                'scan_requests': scan_requests,
                'promocodes': promocodes
            })
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
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/form-admin')
            else:
                return render(request, 'admin-panel/pages/login_page.html', {
                    'login_error': 'Пользователя не существует'})
        else:
            return render(request, 'admin-panel/pages/login_page.html', {
                'login_error': 'Пользователя не существует'})


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
                return render(request, 'admin-panel/pages/admin.html', {
                    'result': f'Код для регистрации: {code}'})
            else:
                return render(request, 'admin-panel/pages/admin.html', {
                    'result': 'Код для этого пользователя уже зарегестрирован'}
                )


def admin_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password'].replace(' ', '')
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
            track = Track.objects.get(pk=id)
            track.name = request.POST.get('new_track_name_{}'.format(id),None)
            track.save()
            current_request = DocsRequest.objects.get(pk=name)

            pasp_info = PaspInfo.objects.get(email=current_request.email)
            print(pasp_info)
            tracks = Track.objects.filter(request=current_request).all()
            return render(
                    request, 'admin-panel/pages/submit.html', {
                        'request': current_request,
                        'tracks': tracks,
                        'pasp_info': pasp_info})
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

                pasp_info = PaspInfo.objects.get(email=current_request.email)
                print(pasp_info)
                tracks = Track.objects.filter(request=current_request).all()
                return render(
                    request, 'admin-panel/pages/submit.html', {
                        'request': current_request,
                        'tracks': tracks,
                        'pasp_info': pasp_info})
            else:
                APP_TOKEN = 'AgAAAAAVXvrzAAZUx8r6G2rp3EZGpwXtTZI4KNg'
                y = yadisk.YaDisk(token=APP_TOKEN)
                doc = DocxTemplate("Music/static/documents/template2.docx")
                request_id = request.POST.get('ID',None)
                sum_request = DocsRequest.objects.get(pk=request_id)
                for track in Track.objects.filter(request=sum_request).all():
                    if request.POST.get('new_track_name_{}'.format(track.name)) == request.POST.get('old_track_name_{}'.format(track.name)):
                        pass
                    else:
                        track.name = request.POST.get('new_track_name_{}'.format(track.name))
                        track.save()
                try:
                    pasp_info = PaspInfo.objects.get(email=sum_request.email)
                except:
                    pasp_info = PaspInfo()
                    pasp_info.full_name = request.POST['FULLNAME']
                    pasp_info.country = request.POST['COUNTRY']
                    pasp_info.serie_num = request.POST['SERIE_NUM']
                    pasp_info.email = sum_request.email
                    pasp_info.who_given = request.POST['GIVEN_BY']
                    pasp_info.when_given = request.POST['GIVEN_DATE']
                    pasp_info.data_born = request.POST['BIRTH_DATE']
                    pasp_info.reg = request.POST['REGISTRATION']
                    pasp_info.save()
                count = len(Counter.objects.filter(number=sum_request.number)) + 1
                context = {
                    'NAME': request.POST['NAME'],
                    'FULL_NAME': request.POST['FULLNAME'],
                    'EMAIL': request.POST['EMAIL'],
                    'COUNTRY': request.POST['COUNTRY'],
                    'BIRTH_DATE': request.POST['BIRTH_DATE'],
                    'NUMBER': f'{sum_request.number}-{count}',
                    'INITIALS': request.POST['INITIALS'],
                    'PASPORT_SERIE': request.POST.get('PASSPORT_SERIE', 'Нет'),
                    'GIVEN_BY': request.POST['GIVEN_BY'],
                    'GIVEN_DATE': request.POST['GIVEN_DATE'],
                    'REGISTRATION': request.POST['BIRTH_PLACE'],
                    'VK': sum_request.contact,
                    'MONTH': f'{months[datetime.now().month]} ',
                    'IMAGE': InlineImage(
                        doc, sum_request.cover.path, width=Mm(50),height=Mm(50)),
                    "DAY": datetime.now().day,
                    'YEAR': datetime.now().year,
                    'TRACKS': Track.objects.filter(request=sum_request).all(),
                    'track_num': [i for i in range(len(list(
                        Track.objects.filter(request=sum_request).all())))]
                }
                print("Cover path:", sum_request.cover.path)
                name = sum_request.release_name

                folder = sum_request.artisi_name+' - '+name
                folder_path = f"/ДИСТРИБУЦИЯ VAUVISION/Заявки на загрузку/{folder}"
                offer_name = f'offer__vauvision__{sum_request.number}-{count}'
                try:
                    doc.render(context)
                except:
                    context['IMAGE'] = 'Вставьте обложку релиза'
                    doc.render(context)

                doc.save(f"Music/static/documents/{offer_name}.docx")
                y.upload(path_or_file=f"Music/static/documents/{offer_name}.docx",
                         dst_path=f'{folder_path}/{offer_name}.docx/')
                path = '{}/Music/static/documents/{}.docx'.format(
                    str(os.path.abspath('')), offer_name)
                filepath = '{}/Music/static/documents/{}.pdf'.format(
                    str(os.path.abspath('')), offer_name)
                _ = subprocess.check_output(
                    ['libreoffice', '--convert-to', 'pdf', path])
                time.sleep(5)
                os.rename('{}/{}.pdf'.format(str(os.path.abspath('')),offer_name), '{}/Music/static/documents/{}.pdf'.format(str(os.path.abspath('')),offer_name))
                y.upload(path_or_file=f"Music/static/documents/{offer_name}.pdf",
                         dst_path=f'{folder_path}/{offer_name}.pdf/')

                addr_from = "vau@vauvision.com"  # Отправитель
                password = "20052005Vauvision!"
                addr_to = request.POST['EMAIL']

                msg = MIMEMultipart()  # Создаем сообщение
                msg['From'] = addr_from  # Адресат
                msg['To'] = addr_to  # Получатель
                msg['Subject'] = "{}. Договор на дистрибуцию VAUVISION.".format(request.POST['FULLNAME'])  # Тема сообщения

                body = render_to_string('email.txt', {
                    'full_name': request.POST['FULLNAME']})

                msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

                ctype, encoding = mimetypes.guess_type(filepath)
                maintype, subtype = ctype.split('/', 1)
                with open(filepath, 'rb') as fp:
                    file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                    file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                    fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
                file.add_header('Content-Disposition', 'attachment', filename=str(offer_name+'.pdf'))  # Добавляем заголовки
                msg.attach(file)

                server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
                # server.starttls()
                server.login(addr_from, password)
                server.send_message(msg)
                server.quit()
                current_request = DocsRequest.objects.filter(id=request_id).delete()

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
                Track.objects.filter(request=current_request).delete()
                current_request.delete()
            return redirect('/form-admin')
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')


def createcode(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                code = PromoCodes.objects.create(
                    name=request.POST.get('code_name',None),
                    value=request.POST.get('value',None)
                )
                code.save()
            return redirect('/form-admin')
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')


def deletecode(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                PromoCodes.objects.filter(name=request.POST.get('delete_code',None)).delete()
            return redirect('/form-admin')
        else:
            return redirect('/form-admin/login/')
    else:
        return redirect('/form-admin/login/')




'''APP_TOKEN = 'AgAAAAA_8uwPAAarbHv2-khOnkCRmzitHRkTKdU'
    y = yadisk.YaDisk(token=APP_TOKEN)

    artistName = request.POST['artistName']
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

        addr_from = "vau@vauvision.com"  # Отправитель
        password = "20052005Vauvision!"
        addr_to = email

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = "Аккаунт VAUVISION успешно создан!"  # Тема сообщения

        body = 'Добрый день!' + "Вы отправили заявку на дистрибуцию на лейбле VAUVISION.\n\n Теперь у вас на сайте есть личный кабинет, где вы можете видеть свои загруженные релизы, договоры, получить отчёты о прослушиваниях и прочую информацию. Функционал кабинета постепенно будет пополняться. \n\n\n Логин: {} \n Пароль: {} \n\n\n Пожалуйста, сохраните логин и пароль от личного кабинета.Скоро на почту придет письмо с договором и дальнейшие инструкции.\n\n По всем возникающим вопросам пишите в личные сообщения https://vk.com/vauvision или https://vk.com/vauvisionlabel".format(
            email, generated_pass)  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        # server.starttls()
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
            new_track.release_date = releaseDate
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

    return redirect('https://vk.com/vauvisionlabel/')'''


@require_http_methods(["POST"])
def form_push(request):
    if not request.user.is_authenticated:
        return redirect('/')

    form = request.POST

    return HttpResponse()
