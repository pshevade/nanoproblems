# django secret

from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

DJANGO_SECRET = get_random_string(50, chars)
