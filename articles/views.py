#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from django.core.management import call_command

from django.shortcuts import render
from django.http import Http404
from markdown import markdown

from articles.models import Share, Resources
from articles.models import Article

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def essays_preview(request):
    article_list = Article.objects.all().order_by("-time")
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    try:
        onepage_articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        onepage_articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        onepage_articles = paginator.page(paginator.num_pages)
    for article in onepage_articles:
        article.body = markdown(article.body,
                                extensions=['codehilite'],
                                extension_configs={'codehilite': [('linenums', True),
                                                                  ('noclasses', True),
                                                                  ('pygments_style', 'native')]})
    context = {'all_essays': article_list,
               'onepage_essays': onepage_articles}
    return render(request, 'essays_preview.html', context)


def essays_detail(request, essay_id):
    article_list = Article.objects.all().order_by("-time")
    try:
        article = Article.objects.get(id=essay_id)
        article.body = markdown(article.body,
                                extensions=['codehilite'],
                                extension_configs={'codehilite': [('linenums', True),
                                                                  ('noclasses', True),
                                                                  ('pygments_style', 'native')]})
    except Article.DoesNotExist:
        raise Http404
    context = {'all_essays': article_list,
               'essay': article}
    return render(request, 'essays_detail.html', context)


def about(request):
    return render(request, 'about.html')


def share(request):
    shares = Share.objects.all().order_by("-updated")
    paginator = Paginator(shares, 5)
    page = request.GET.get('page')
    try:
        onepage_shares = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        onepage_shares = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        onepage_shares = paginator.page(paginator.num_pages)
    for s in onepage_shares:
        s.body = markdown(s.body,
                          extensions=['codehilite'],
                          extension_configs={'codehilite': [('linenums', True),
                                                            ('noclasses', True),
                                                            ('pygments_style', 'native')]})
    context = {"shares": onepage_shares}
    return render(request, 'share.html', context)


def tag_search(request, tag):
    # todo： user update time
    article_list = Article.objects.all().order_by("-time")
    articles = Article.objects.filter(tags__name=tag)
    shares = Share.objects.filter(tags__name=tag)
    for s in shares:
        s.body = markdown(s.body,
                          extensions=['codehilite'],
                          extension_configs={'codehilite': [('linenums', True),
                                                            ('noclasses', True),
                                                            ('pygments_style', 'native')]})
    context = {'all_essays': article_list,
               'articles': articles,
               'shares': shares,
               'tag': tag}
    return render(request, 'search.html', context)


def home(request):
    imgs = Resources.objects.filter(is_show=True, is_uploaded=True)
    imgs = [x.file_name for x in imgs]
    imgs_show = []
    for i in range(3):
        imgs_show.append(random.choice(imgs))
    context = {'imgs': imgs_show}
    return render(request, 'home.html', context)


# process form
def search(request):
    keywords = request.GET['keywords']
    articles = Article.objects.filter(body__icontains=keywords).order_by('-time')
    shares = Share.objects.filter(body__icontains=keywords).order_by('-time')
    context = {'tag': keywords,
               'shares': shares,
               'articles': articles}
    return render(request, 'search.html', context)

def projects(request):
    articles = Article.objects.all().order_by('-time')
    context = {'articles': articles}
    return render(request, 'projects.html')
