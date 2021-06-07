from django.db import models
from django.contrib.auth.models import User
class AuthUser(User):
    def natural_key(self):
        return self.username

class Message(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Sender')
    Receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Receiver')
    Message = models.CharField(max_length=500)
    Subject = models.CharField(max_length=100)
    CreationDate = models.DateTimeField()
    Readed = models.BooleanField()   
