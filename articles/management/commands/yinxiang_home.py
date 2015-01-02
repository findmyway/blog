#!/usr/bin/env python
# -*- coding: utf-8 -*-

from evernote.api.client import EvernoteClient, NoteStore
from django.core.management.base import BaseCommand
from django.conf import settings
import time
from articles.models import Resources


class Command(BaseCommand):
    target_book = settings.NOTEBOOK_HOME
    evernote_token = settings.EVERNOTE_TOKEN
    client = EvernoteClient(token=evernote_token,
                            sandbox=False,
                            service_host='app.yinxiang.com')
    noteStore = client.get_note_store()
    userStore = client.get_user_store()
    user_info = userStore.getPublicUserInfo('tianjun_cpp')

    def handle(self, *args, **options):
        print('+++++++++' + time.ctime() + '+++++++++++')
        local_show_imgs = {x.evernote_guid: x
                           for x in Resources.objects.filter()}
        remote_show_imgs = self.get_remote_show_imgs()
        for res in remote_show_imgs:
            if res.guid in local_show_imgs.keys():
                r = local_show_imgs[res.guid]
                r.is_show = True
                r.save()
            else:
                res_hex_hash = ''.join(["%02X" % (ord(x)) for x in res.data.bodyHash]).lower()
                file_name = unicode(res.attributes.fileName, 'utf-8')
                r = Resources(evernote_guid=res.guid,
                              file_name=file_name + '_' + res_hex_hash,
                              hex_hash=res_hex_hash,
                              is_show=True
                )
                r.save()

        self.stdout.write("SUCCESS!")

    def get_remote_show_imgs(self):
        notebooks = self.noteStore.listNotebooks()
        target_book_guid = None
        for n in notebooks:
            if n.name == self.target_book:
                target_book_guid = n.guid
                break
        filter = NoteStore.NoteFilter()
        filter.notebookGuid = target_book_guid
        spec = NoteStore.NotesMetadataResultSpec()
        spec.includeUpdated = True
        mylist = self.noteStore.findNotesMetadata(self.evernote_token, filter, 0, 10000, spec)
        img_resources = []
        for note in mylist.notes:
            note_detail = self.noteStore.getNote(self.evernote_token, note.guid, True, False, False, False)
            for res in note_detail.resources:
                img_resources.append(res)
        return img_resources
