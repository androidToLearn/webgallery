from .models import User
import uuid
import json
import random
import os
from django.core.mail import EmailMessage
from .models import Image
import ssl
import smtplib


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
                       'color': user.color, 'mac': user.mac}, file, indent=4)

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
        json = {'image_name': image.image.name, 'image_url': image.image.url, 'date': image.date, 'owner': image.owner,
                'userName': image.userName, 'accessNames': image.accessNames, 'isFavorite': image.isFavorite, 'isShared': (not image.accessNames[0] == image.owner)}
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
