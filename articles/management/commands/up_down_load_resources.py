#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5

from django.core.management.base import BaseCommand
from evernote.api.client import EvernoteClient
import requests
import qiniu
from qiniu import etag
from django.conf import settings
import time
from articles.models import Resources


class Command(BaseCommand):
    evernote_token = settings.EVERNOTE_TOKEN
    client = EvernoteClient(token=evernote_token,
                            sandbox=False,
                            service_host='app.yinxiang.com')
    noteStore = client.get_note_store()
    userStore = client.get_user_store()
    user_info = userStore.getPublicUserInfo('tianjun_cpp')

    q = qiniu.Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)

    def handle(self, *args, **options):
        # local_resources = os.listdir(resources_dir)
        print('+++++++++' + time.ctime() + '+++++++++++')
        for r in Resources.objects.filter(is_downloaded=False):
            res_url = "%sres/%s" % (self.user_info.webApiUrlPrefix, r.evernote_guid)
            res_name =r.file_name
            try:
                resp = requests.post(res_url, data={'auth': self.evernote_token})
                resp_build_hash = md5()
                resp_build_hash.update(resp.content)
                resp_hash = resp_build_hash.hexdigest()
                if resp_hash == r.hex_hash:
                    with open(settings.RESOURCES_DIR + res_name, 'wb') as f:
                        f.write(resp.content)
                    r.is_downloaded = True
                    r.save()
            except Exception, e:
                # todo log error
                print(u'Download {} failed'.format(res_name))

        for r in Resources.objects.filter(is_downloaded=True, is_uploaded=False):
            res_name = r.file_name
            qiniu_token = self.q.upload_token(settings.BUCKET_NAME, settings.QINIU_PREFIX + res_name.encode('utf-8'))
            try:
                ret, info = qiniu.put_file(qiniu_token, settings.QINIU_PREFIX + res_name,
                                           settings.RESOURCES_DIR + res_name,
                                           check_crc=True)
                if ret.get('hash', '') == etag(settings.RESOURCES_DIR +res_name):
                    r.is_uploaded = True
                    r.save()
            except Exception, e:
            # todo log error
                print(u'Upload {} failed'.format(res_name))

        print("SUCCESS!")




