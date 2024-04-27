import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User

class UserDetails(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    bod = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    photo = models.FileField(upload_to='Photo', null=True, blank=True)
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "User Detail"
        db_table = "User Detail"
       
class OtpCode(models.Model):
    code = models.CharField(max_length=100)
    is_used = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_status(self):
        date = datetime.datetime(self.date_created.year, self.date_created.month, self.date_created.day, self.date_created.hour +3, self.date_created.minute, self.date_created.second)

        if date > self.date_created:
            return 'Valid'
        else:
            return 'Invalid'

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "OtpCode"
        db_table = "OtpCode"
