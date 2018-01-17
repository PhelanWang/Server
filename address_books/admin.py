# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from address_books.models import Category, Entry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass
