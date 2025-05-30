import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import FormImage, FormUser
from .models import Image, User, Date
from .helpViews import helpVies
import uuid
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import FileResponse, HttpResponse
import random
from datetime import datetime, timedelta
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
        if myJson['name'] == '' or myJson['name'] in image.accessNames:
            # bad name finish method
            return JsonResponse({'r': 'bad'})
        image.accessNames.append(myJson['name'])
        date = datetime.now().strftime('%d%m%Y')

        Date.objects.create(image=image.image, date=date,
                            owner=myJson['name'], numfile=image.numfile)
        image.save()
        print('shared')
    return JsonResponse({'r': myJson['name']})


def getObjectImageByname(images, imageName, owner):
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


def custom_upload_to(instance, filename):
    ext = filename.split('.')[-1]  # סיומת הקובץ
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}.{ext}"
    return os.path.join('images', filename)


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
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%d%m%Y')
            yesterday1 = (datetime.now() - timedelta(days=2)
                          ).strftime('%d%m%Y')

            Image.objects.create(image=img, userName=user.name,
                                 accessNames=[user.name], date=yesterday1, owner=user.name, numfile=len(Image.objects.all()))
        return redirect('index1')
    else:
        user = helpVies.getUser()

        images = Image.objects.all()

        images = helpVies.getOnlyMyImagesAndShared(images, user)

        images = helpVies.copyWithSharedAsRealDate(images)
        formImage = FormImage()
        rows = []
        video_extensions = ('.mp4', '.webm', '.avi', '.mov')
        keepi = -1
        isTODoNewLine = 0
        row = []
        isStart = True
        indexInsert = -1
        isInserted = False
        # הערך הזה שומר את השורה א=האחרונה של היום האחרון שבו המשתמש העלה דברים keepEndLine

        while keepi < len(images):
            # לבדוק נוספו לאחרונה ולהוסיף /
            # לשנות להיום אתמול
            keepi += 1

            print('------------------------')
            if keepi < len(images):
                print(images[keepi].date)
            if keepi + 1 < len(images):
                print(images[keepi + 1].date)
            if keepi + 1 < len(images) and images[keepi].date != images[keepi + 1].date:
                print('inside')
                print('----------------------')
                # כל פריט עם date אחר אחריו
                row.append({'image': helpVies.toJson(images[keepi]), 'isVideo': images[keepi].image.name.lower(
                ).endswith(video_extensions), 'type': returnType(images[keepi].image.name.lower(), video_extensions),
                    'isShared': isFirstNameIsNotMe(images[keepi]), 'time_shared': findImageByImage(Date.objects.all(), images[keepi]), 'isNewDate': isStart})
                isStart = False
                keepi += 1
                indexInsert += 1
                # סוף השורה הקודמת - שורה רגילה
                rows.insert(indexInsert, row)
                row = []
                isTODoNewLine = 0
                row.append({'image': helpVies.toJson(images[keepi]), 'isVideo': images[keepi].image.name.lower(
                ).endswith(video_extensions), 'type': returnType(images[keepi].image.name.lower(), video_extensions),
                    'isShared': isFirstNameIsNotMe(images[keepi]), 'time_shared': findImageByImage(Date.objects.all(), images[keepi]), 'isNewDate': True})
                indexInsert = -1
                isStart = False
                isTODoNewLine = 1
                isInserted = True
                keepi -= 1

            elif not isInserted and keepi < len(images):
                # האחרון וכל פריט אחר שאין date אחר אחריו
                row.append({'image': helpVies.toJson(images[keepi]), 'isVideo': images[keepi].image.name.lower(
                ).endswith(video_extensions), 'type': returnType(images[keepi].image.name.lower(), video_extensions),
                    'isShared': isFirstNameIsNotMe(images[keepi]), 'time_shared': findImageByImage(Date.objects.all(), images[keepi]), 'isNewDate': isStart})
                isStart = False
                isTODoNewLine += 1
            if isTODoNewLine == 5:
                # סוף  5 פריטים
                indexInsert += 1
                rows.insert(indexInsert, row)
                row = []
                isTODoNewLine = 0
            isInserted = False
        if len(row) > 0:
            # בסוף זה עושה את של היום
            indexInsert += 1
            rows.insert(indexInsert, row)

        yesterday = datetime.now() - timedelta(days=1)
        hasToday = helpVies.isHasTodayImg(images)
        noEmail = (user.email == '')
        if os.path.exists(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json')):
            with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'r') as file:
                noEmail = json.load(file)['isHas']
        with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'w') as file:
            json.dump({'isHas': (noEmail - 1)}, file, indent=4)
        noEmail = (noEmail > 0)
        print('noEmail', noEmail)
        # צריך שיהיה משהו בלי רווח מלמעלה בהתחלה יכול להיות today ויכול להיות yesterday

        return render(request, 'app/page1.html', {'form': formImage, 'rows': json.dumps(rows), 'rows_not_json': rows, 'user': user.name[0], 'color': user.color, 'usern': user.name, 'date': datetime.now().strftime('%d%m%Y'), 'datey': yesterday.strftime('%d%m%Y'), 'isHaveIdentify': json.dumps(noEmail), 'hasTodayImg': hasToday, 'hasYesterdayImgOrToday': (helpVies.isHasYesterdayImg(images) or hasToday), 'hasTodayImg1': json.dumps(hasToday), 'hasYesterdayImgOrToday1': json.dumps((helpVies.isHasYesterdayImg(images) or hasToday))})


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

        if isForget == 1:
            b = False
            # כניסה עם משתמש לפי אימייל קיים של המשתמש
            for user in User.objects.all():
                if user.email == json1['email']:
                    # בשביל אימות משתמש
                    helpVies.saveUser(user)
                    b = True

            if not b:
                return JsonResponse({'r': 'האימייל לא קיים במערכת'})
        # אימות משתמש עם האימייל שלו
        i = random.randint(1000, 9999)
        helpVies.saveCodeToFiles(i)
        user = helpVies.getUser()
        user.email = json1['email']
        user.save()
        helpVies.saveUser(user)
        return JsonResponse({'code': i, 'email': json1['email'], 'name': helpVies.getUser().name, 'password': helpVies.getUser().password})
    return JsonResponse({'r': 'nothing'})


@csrf_exempt
def moveToChangePassword(request):
    # get email from savedUser...
    # get number from files json
    if request.method == 'POST':
        i = helpVies.getCodeFromFiles()
        jsonPassword = json.loads(request.body)

        try:
            if int(jsonPassword['password']) == i:
                print('good')
                return JsonResponse({'r': 'good'})
            else:
                print('bad')
                return JsonResponse({'r': 'bad code'})
        except Exception as e:
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
            if user.email == '':
                i = 2
            else:
                i = 0
            with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'w') as file:
                json.dump({'isHas': i}, file, indent=4)
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
            helpVies.saveUser(user)
            if user.email == '':
                i = 2
            else:
                i = 0
            with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'w') as file:
                json.dump({'isHas': i}, file, indent=4)
            return redirect('index1')
        print('bad')
        return render(request, 'app/badName.html', {})
    else:
        print(len(User.objects.all()))
        user = helpVies.getExistsUserwithMac()
        if user != None:
            print('in with mac')
            helpVies.saveUser(user)
            if user.email == '':
                i = 2
            else:
                i = 0
            with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'w') as file:
                json.dump({'isHas': i}, file, indent=4)
            return redirect('index1')
        print('not with mac')
        return render(request, 'app/loginPage.html', {'user': ''})


def loginPageNew(request):
    print('login page new user')
    user = helpVies.getUser()
    if user.email == '':
        i = 2
    else:
        i = 0
    with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/fileisHas' + str(uuid.getnode()) + '.json'), 'w') as file:
        json.dump({'isHas': i}, file, indent=4)
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
