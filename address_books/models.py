# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# 分组模型
class Category(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='categorys', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.text


# 联系人条目
class Entry(models.Model):
    phone_number = models.CharField(max_length=11)
    name = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name + "    " + self.phone_number
