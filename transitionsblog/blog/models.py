
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField


# Create your models here.


class Post(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    image_url = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    active = models.BooleanField(default=False)


    class Meta:
        ordering: ['-date']
   
    def __str__(self):
        return self.title





