import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import FormImage, FormUser
from .models import Image, User, Date
from .helpViews import helpVies
import uuid
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import FileResponse
import random
from datetime import datetime
import requests
from django.conf import settings


def index1_new_user(request):
    user = helpVies.getUser()
    return render(request, 'app/loginPage.html', {'user': user.email})


@csrf_exempt
def share_image(request):
    if request.method == 'POST':
        myJson = json.loads(request.body)
        image = getObjectImageByname(
            Image.objects.all(), myJson['image'], myJson['owner'])
        if myJson['name'] == '':
            return JsonResponse({'r': 'ok'})
        image.accessNames.append(myJson['name'])
        date = datetime.now().strftime('%d%m%Y')
        Date.objects.create(image=image.image, date=date)
        image.save()
        print('shared')
    return JsonResponse({'r': 'ok'})


def getObjectImageByname(images, imageName, owner):
    print('---------------')
    print(imageName)
    print(owner)
    for image in images:
        if image.image.name == imageName and image.owner == owner:
            return image


@csrf_exempt
def download(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            relative_path = data['url']  # לדוגמה: 'images/icon23.jpg'

            file_path = r'C:\Users\rachm\OneDrive\שולחן העבודה\test2\gallery\app' + \
                '\\' + 'media\\' + relative_path.replace('/', '\\')
            print(file_path)
            path = file_path
            print(path)
            if os.path.exists(path):
                print('found')
                return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            else:
                print('not found')
                return JsonResponse({'error': 'file not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'invalid method'}, status=405)


@csrf_exempt
def index1(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        all = []
        user = helpVies.getUser()
        print('size' + str(len(images)))
        for img in images:
            print(img)
            date = datetime.now().strftime('%d%m%Y')
            Image.objects.create(image=img, userName=user.name,
                                 accessNames=[user.name], date=date, owner=helpVies.getUser().name)
        return redirect('index1')
    else:
        user = helpVies.getUser()
        images = Image.objects.all()
        images = helpVies.getOnlyMyImagesAndShared(images, user)
        formImage = FormImage()
        rows = []
        video_extensions = ('.mp4', '.webm', '.avi', '.mov')
        for j in range(0, len(images), 5):
            row = []

            for i in range(j, j + 5):
                if i < len(images):
                    row.append({'image': helpVies.toJson(images[i]), 'isVideo': images[i].image.name.lower(
                    ).endswith(video_extensions), 'type': returnType(images[i].image.name.lower(), video_extensions),
                        'isShared': isFirstNameIsNotMe(images[i]), 'time_shared': findImageByImage(Date.objects.all(), images[i])})

            rows.append(row)

        return render(request, 'app/page1.html', {'form': formImage, 'rows': json.dumps(rows), 'rows_not_json': rows, 'user': user.name[0], 'color': user.color, 'usern': user.name, 'date': datetime.now().strftime('%d%m%Y')})


def findImageByImage(dates_shared, image):
    for date_o in dates_shared:
        if date_o.image == image.image:
            return date_o.date
    return None


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        password = json.loads(request.body)['password']
        user = helpVies.getUser()
        user.password = password
        user.save()
        return JsonResponse({})


@csrf_exempt
def to_favorite(request):
    if request.method == 'POST':
        name1 = json.loads(request.body)['name']
        owner1 = json.loads(request.body)['owner']
        images = helpVies.getAllImagesBy(owner1, name1)
        print('size', str(len(images)))
        for img in images:
            img.isFavorite = True
            img.save()
    return JsonResponse({})


def isFirstNameIsNotMe(image):
    """בודק שהשם accessNames הראשון הוא לא אני"""
    return not image.accessNames[0] == helpVies.getUser().name


def returnType(name, video_extensions):
    for ex in video_extensions:
        if '.' + name.split('.', 1)[1] == ex:
            return name.split('.', 1)[1]
    return None


def getImage(request, file):
    return FileResponse(open(file.path, 'rb'),  as_attachment=True, filename=file.name+'.png')


def pageImage(request):
    return render(request, 'app/pageImage.html')


def to_change_password(request, isForget):
    return render(request, 'app/restartPassword.html', {'isForget': isForget})


@csrf_exempt
def sendEmailWithJsonToNextPage(request, isForget):
    if request.method == 'POST':

        json1 = json.loads(request.body)
        print(json1)

        print('isForget', str(isForget))
        if isForget == 1:
            b = False
            # כניסה עם משתמש לפי אימייל קיים של המשתמש
            for user in User.objects.all():
                if user.email == json1['email']:
                    # בשביל אימות משתמש
                    helpVies.saveUser(user)
                    b = True

            if not b:
                print('inside bad gmail')
                return JsonResponse({'r': 'האימייל לא קיים במערכת'})
        # אימות משתמש עם האימייל שלו
        i = random.randint(1000, 9999)
        helpVies.saveCodeToFiles(i)
        user = helpVies.getUser()
        user.email = json1['email']
        user.save()
        print('finish')
        return JsonResponse({'code': i, 'email': json1['email'], 'name': helpVies.getUser().name, 'password': helpVies.getUser().password})
    return JsonResponse({'r': 'nothing'})


@csrf_exempt
def moveToChangePassword(request):
    # get email from savedUser...
    # get number from files json
    if request.method == 'POST':
        i = helpVies.getCodeFromFiles()
        jsonPassword = json.loads(request.body)

        # print('inside test code')
        print(jsonPassword['password'])
        if int(jsonPassword['password']) == i:
            print('good')
            return JsonResponse({'r': 'good'})
        else:
            print('bad')
            return JsonResponse({'r': 'bad code'})
    return JsonResponse({'r': 'nothing'})


@csrf_exempt
def we(request):
    return JsonResponse({'r': 'good'})


@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = helpVies.isExistsUser(data['name'], data['password'])
        if user != None:
            helpVies.saveUser(user)
            return redirect('index1')
        if helpVies.isGoodName(data['name']):
            print('create')
            # when new two user in same computer the color appear or create , and the first enter automaticly
            user = User.objects.create(
                name=data['name'], password=data['password'], color=data['color'], mac=uuid.getnode(), email='')
            print(User.objects.all()[0].color)
            user = User()
            user.name = data['name']
            user.password = data['password']
            user.color = data['color']
            user.mac = uuid.getnode()
            helpVies.saveUser(user)
            return redirect('index1')
        return JsonResponse({'response': 'bad name'})
    else:
        print(len(User.objects.all()))
        user = helpVies.getExistsUserwithMac()
        if user != None:
            print('in with mac')
            helpVies.saveUser(user)
            return redirect('index1')
        print('not with mac')
        return render(request, 'app/loginPage.html', {'user': ''})


def loginPageNew(request):
    return render(request, 'app/loginPage.html', {'user': ''})


@csrf_exempt
def to_delete(request):
    if request.method == 'POST':
        name1 = json.loads(request.body)['name']
        owner1 = json.loads(request.body)['owner']
        # תמיד יוצא image 1 בלבד כי לכל image יש שם אחר
        images = helpVies.getAllImagesBy(owner1, name1)
        user = helpVies.getUser()

        for img in images:
            print(img)
            if not img.accessNames[0] == user.name:
                img.accessNames.remove(user.name)
                img.save()
            else:
                img.delete()

    return JsonResponse({})


def insertColor(color):
    helpVies.insertColorToFiles(color)


def custom404(request, exception=None):
    return render(request, 'app/404.html', status=404)
