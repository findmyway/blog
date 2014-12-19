#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.encoding import smart_unicode
from django.contrib import admin
from django.db import models

from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.TextField()
    body = models.TextField()
    time = models.DateTimeField()
    # for evernote
    updated = models.DateTimeField(blank=True, null=True)
    evernote_guid = models.TextField(blank=True, null=True)

    tags = TaggableManager()

    def __unicode__(self):
        return smart_unicode(self.title)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'time', 'updated', 'evernote_guid']


class Share(models.Model):
    time = models.DateTimeField()
    body = models.TextField()
    updated = models.DateTimeField(blank=True, null=True)
    evernote_guid = models.TextField(blank=True, null=True)
    tags = TaggableManager()

    def __unicode__(self):
        return smart_unicode(self.body)


class ShareAdmin(admin.ModelAdmin):
    list_display = ['time']


class Resources(models.Model):
    evernote_guid = models.TextField()
    file_name = models.TextField()
    hex_hash = models.TextField()

    is_downloaded = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)

    def __unicode__(self):
        return smart_unicode(self.file_name)


class ResourcesAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'is_show', 'is_downloaded', 'is_uploaded']

