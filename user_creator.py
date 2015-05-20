import random
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djapp.settings")
import django
django.setup()

from django.contrib.auth.hashers import make_password
from elect.models import User

members = ['alex','arielle','char','dan','jamie','jewel','jid','jona','keirin','ken','kim','lance','lora','lucas','mar','marco','mika','muffin','ona','pearl','raiki','sapot','tasha','walter','ysa']

print (str("Total-members,")+str(len(members)))
letters = map(chr,range(97,123))
for member in members:
    password = ""
    for i in range(8):
        new = random.choice(letters)
        while len(password) != 0 and new == password[-1]:
            new = random.choice(letters)
        password += new
    hash = make_password(password)
    if len(User.objects.filter(username=member)) != 0:
        print (member+",ERROR")
    else:
        print str(member+","+password)
        User.objects.get_or_create(username=member, email="", password=hash)