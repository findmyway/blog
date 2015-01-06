#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.encoding import smart_unicode
from django.contrib import admin
from django.db import models
from django.contrib.syndication.views import Feed
from markdown import markdown
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.TextField()
    body = models.TextField()
    time = models.DateTimeField()
    # for evernote
    updated = models.DateTimeField(blank=True, null=True)
    evernote_guid = models.TextField(blank=True, null=True)

    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return smart_unicode(self.title)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'time', 'updated', 'evernote_guid']


class Share(models.Model):
    time = models.DateTimeField()
    body = models.TextField()
    updated = models.DateTimeField(blank=True, null=True)
    evernote_guid = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)

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


class BlogFeed(Feed):
    title = "TianJun . Machine Learning"
    description = u"自由~ 分享~~ 交流~~~"
    link = "http://www.tianjun.ml/blog/feed/"
    item_author_name = u'田俊'

    def items(self):
        return Article.objects.all().order_by("-updated")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.body,
                        extensions=['codehilite'],
                        extension_configs={'codehilite': [('linenums', True),
                                                          ('noclasses', True),
                                                          ('pygments_style', 'native')]})

    def item_link(self, item):
        return u"http://tianjun.ml/essays/%d" % item.id

