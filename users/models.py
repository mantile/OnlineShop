from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    user_first_name = models.CharField(max_length=50, blank=True)
    user_last_name = models.CharField(max_length=50, blank=True)
    user_mail = models.EmailField(unique=True, blank=True)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Check yours number - its not correct: format is +99999999999 of 99999999999, from 9 to 15 numbers'
    )

    phone_number = models.CharField(validators=[phone_validator], max_length=17, blank=True)

    def __str__(self):
        return self.user.username