from django.contrib.auth.models import User
from django.db import models

import datetime
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Category', max_length=200)
    description = models.TextField('Text')

class Petition(models.Model):
    title = models.CharField('Petition', max_length=200)
    text = models.TextField('Text')
    image = models.ImageField('Image', upload_to='media/')
    datetime_created = models.DateTimeField('Datetime created', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    voters = models.ManyToManyField(User, related_name='voter')

    def IsExpired(self):
        return self.datetime_created >= (timezone.now() - datetime.timedelta(days=14))

    def VoteCount(self):
        return self.voters.all().count()

    def HasPassed(self):
        return self.IsExpired() and (self.VoteCount() >= 200)

    #Count: Petition.objects.count()