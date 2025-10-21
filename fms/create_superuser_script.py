import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fms.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'mico'
email = 'faithmico4@gmail.com'
password = 'm1co2o25'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created')
else:
    print('User already exists')
