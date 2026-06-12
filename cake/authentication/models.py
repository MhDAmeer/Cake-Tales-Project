from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin','Admin'

    USER = 'User','User'


class Profile(AbstractUser):

    role = models.CharField(max_length=10,choices=RoleChoices.choices)

    class Meta:

        verbose_name = 'Profiles'

        verbose_name_plural = 'Profiles'

    def __str__(self):
        
        return self.username
    
class OTP(models.Model):

    user = models.OneToOneField('Profile',on_delete=models.CASCADE)

    otp = models.CharField(max_length=4)

    otp_verified = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'OTPs'

        verbose_name_plural = 'OTPs'

    def __str__(self):
        
        return f'{self.user.username} otp'