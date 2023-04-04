import uuid
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True, null=False, default=str(uuid.uuid4().hex))
    email = models.EmailField(null=False, unique=True)
    firstname = models.CharField(max_length=20, null=False)
    lastname = models.CharField(max_length=20, null=False)
    username = models.CharField(max_length=40, null=False)
    password = models.CharField(max_length=120, null=False)
    verified = models.BooleanField(default=False)
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    otp_value = models.IntegerField(null=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False)