import random
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djapp.settings")
import django
django.setup()

from elect.models import User

members = ['alex','arielle','char','dan','jamie','jewel','jid','jona','keirin','ken','kim','lance','lora','lucas','mar','marco','mika','muffin','ona','pearl','raiki','sapot','tasha','walter','ysa']

answer = raw_input("enable or disable user? (e/d)")
if answer == 'e':
    enable = True
else:
    enable = False

for member in members:
    user = User.objects.get(username=member)
    user.is_active = enable
    user.save()
    print (str(user.username)+" is "+("enabled" if enable else "disabled"))