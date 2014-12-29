#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from django.conf import settings

from MyBaseYinxiangCommond import MyCommand
from articles.models import Share


class Command(MyCommand):
    target_book = settings.NOTEBOOK_SHARE
    local_type = Share

    def update_articles(self, notes, update_type):

        for note in notes:
            note_detail = self.noteStore.getNote(self.evernote_token, note.guid, True, False, False, False)
            print(note_detail.content)
            print(update_type, '-------------')
            note_content_md = self.mark_down(note_detail)
            print(note_content_md)
            note_tags = self.noteStore.getNoteTagNames(self.evernote_token, note_detail.guid)

            if update_type == 'create':
                article = self.local_type(body=note_content_md,
                                          time=time.strftime('%Y-%m-%d %H:%M:%S',
                                                             time.localtime(note_detail.created / 1000)),
                                          updated=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(note_detail.updated / 1000)),
                                          evernote_guid=note_detail.guid)
            elif update_type == 'update':
                article = self.local_type.objects.get(evernote_guid=note_detail.guid)
                article.body = note_content_md
                article.updated = time.strftime('%Y-%m-%d %H:%M:%S',
                                                time.localtime(note_detail.updated / 1000))
            article.save()

            if note_tags:
                article.tags.set(*note_tags)
