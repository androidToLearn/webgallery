from .models import User, Date
import uuid
import json
import random
import os
from django.core.mail import EmailMessage
from .models import Image
import ssl
import smtplib
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


class helpVies:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def isExistsUser(name, password):
        for user in User.objects.all():
            if user.name == name and user.password == password:
                return user
        return None

    @staticmethod
    def saveUser(user):
        with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/savedUser' + str(uuid.getnode()) + '.json'), 'w') as file:
            json.dump({'name': user.name, 'password': user.password,
                       'color': user.color, 'mac': user.mac, 'email': user.email}, file, indent=4)

    @staticmethod
    def isGoodName(name):
        for user in User.objects.all():
            if user.name == name:
                return False
        return True

    @staticmethod
    def getExistsUserwithMac():
        for user in User.objects.all():
            print(user)
            if user.mac == uuid.getnode():
                return user
        return None

    @staticmethod
    def getUser():
        with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/savedUser' + str(uuid.getnode()) + '.json'), 'r') as file:
            data = json.load(file)
            user = User()
            user.name = data['name']
            user.password = data['password']
            user.color = data['color']
            user.mac = data['mac']
            user.email = data['email']
        return user

    @staticmethod
    def getOnlyMyImagesAndShared(images, user):
        newImages = []
        for img in images:
            if user.name in img.accessNames:
                newImages.append(img)
        return newImages

    @staticmethod
    def asJson(bool):
        return {'type': bool}

    @staticmethod
    def toJson(image):
        date_str = image.date
        day = date_str[0:2]
        month = date_str[2:4]
        year = date_str[4:8]
        formatted_date = f"{day}/{month}/{year}"

        json = {'image_name': image.image.name, 'image_url': image.image.url, 'date': image.date, 'owner': image.owner,
                'userName': image.userName, 'accessNames': image.accessNames, 'isFavorite': image.isFavorite, 'isShared': (not image.accessNames[0] == image.owner), 'sdate': formatted_date}
        return json

    @staticmethod
    def sendEmail(i, mail):

        context = ssl._create_unverified_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login("your_email@gmail.com", "app_password")

        email = EmailMessage(
            subject='Gallery',
            body='<h1>'+str(i)+' :קוד האימות שלך הוא </h1>',
            to=[mail],
        )
        email.content_subtype = 'html'
        email.send()

    @staticmethod
    def getCodeFromFiles():
        with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/savedCode' + str(uuid.getnode()) + '.json'), 'r') as file:
            json1 = json.load(file)
        return json1['code']

    @staticmethod
    def saveCodeToFiles(i):
        with open(os.path.join(helpVies.BASE_DIR, 'app', 'data/savedCode' + str(uuid.getnode()) + '.json'), 'w') as file:
            json.dump({'code': i}, file, indent=4)

    @staticmethod
    def getAllImagesBy(owner, name):
        imgs = []
        for img in Image.objects.all():
            if img.image.name == name and owner == img.owner:
                imgs.append(img)
        return imgs

    @staticmethod
    def copyWithSharedAsRealDate(images):

        newImages = []
        user = helpVies.getUser()

        for img in images:
            if img.accessNames[0] == user.name:
                newImages.append(img)
            elif user.name in img.accessNames:
                # תמונה משותפת
                # כיוון שאני לא מכניס אחרכך לsql
                # את הפריטים אין בעייה לשנות את הפרטים שלהם
                img.date = helpVies.getImageFromDatesBy(
                    img.numfile, img.owner).date
                newImages.append(img)
        return newImages

    # להוסיף בimage...good url
    # להוסיף בdate owner

    def getImageFromDatesBy(numfile, owner):
        """""get the specific date object that much to the image in my account"""
        # צריך owner למקרה שתמונה אחת שותפה עם כמה אנשים בשמנים שונים
        for date in Date.objects.all().filter(owner=helpVies.getUser().name):
            # בודק שהimage של השולח שווה באמת לDate שיש לי
            # אז owner צריך להיות שלי
            # כיוון שמיתוך כל הdates שלי אני לוקח את האחד ששייך לimaae הנכון
            if date.numfile == numfile:
                return date
        return None

    def isHasTodayImg(images):
        dateNow = datetime.now().strftime('%d%m%Y')
        for img in images:
            if img.date == dateNow:
                return True
        return False

    def isHasYesterdayImg(images):
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%d%m%Y')
        for img in images:
            if img.date == yesterday:
                return True
        return False
