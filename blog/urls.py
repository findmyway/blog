#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'blog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'articles.views.essays_preview'),
                       url(r'^essays/(?P<essay_id>\d+)/$', 'articles.views.essays_detail'),
                       url(r'^home/$', 'articles.views.home'),
                       url(r'^share/$', 'articles.views.share'),
                       url(r'^about/$', 'articles.views.about'),
                       url(r'^search/$', 'articles.views.search'),
                       url(r'^projects/$', 'articles.views.projects'),
                       url(r'^tag/(?P<tag>\w+)$', 'articles.views.tag_search'),
)
