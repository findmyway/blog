#!/usr/bin/env python
# -*- coding: utf-8 -*-

from articles.models import *


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Resources, ResourcesAdmin)
