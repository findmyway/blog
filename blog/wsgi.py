#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import sys
base = os.path.dirname(os.path.realpath(__file__))
base_par = os.path.dirname(base)

sys.path.append(base_par)
sys.path.append(base)


os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
