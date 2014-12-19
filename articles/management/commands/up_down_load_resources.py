#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5

from django.core.management.base import BaseCommand
from evernote.api.client import EvernoteClient
import requests
import qiniu
from qiniu import etag
from django.conf import settings

from articles.models import Resources


class Command(BaseCommand):
    evernote_token = settings.EVERNOTE_TOKEN
    client = EvernoteClient(token=evernote_token)
    noteStore = client.get_note_store()
    userStore = client.get_user_store()
    user_info = userStore.getPublicUserInfo('tianjun_cpp')

    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)

    def handle(self, *args, **options):
        # local_resources = os.listdir(resources_dir)
        for r in Resources.objects.filter(is_downloaded=False):
            res_url = "%sres/%s" % (self.user_info.webApiUrlPrefix, r.evernote_guid)
            try:
                resp = requests.post(res_url, data={'auth': self.evernote_token})
                resp_build_hash = md5()
                resp_build_hash.update(resp.content)
                resp_hash = resp_build_hash.hexdigest()
                self.stdout.write(resp_hash + "->" + r.hex_hash)
                if resp_hash == r.hex_hash:
                    with open(settings.RESOURCES_DIR + r.file_name, 'wb') as f:
                        f.write(resp.content)
                    r.is_downloaded = True
                    r.save()
            except Exception, e:
                self.stdout.write(e)

        for r in Resources.objects.filter(is_downloaded=True, is_uploaded=False):
            qiniu_token = self.q.upload_token(settings.BUCKET_NAME, settings.QINIU_PREFIX + r.file_name)
            try:
                ret, info = qiniu.put_file(qiniu_token, settings.QINIU_PREFIX + r.file_name,
                                           settings.RESOURCES_DIR + r.file_name,
                                           check_crc=True)
                self.stdout.write(ret.get('hash', '') + "<-qn->" + etag(settings.RESOURCES_DIR + r.file_name))
                if ret.get('hash', '') == etag(settings.RESOURCES_DIR + r.file_name):
                    r.is_uploaded = True
                    r.save()
            except Exception, e:
                self.stdout.write(e)





