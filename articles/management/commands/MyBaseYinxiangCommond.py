#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import HTMLParser
from django.conf import settings
from evernote.api.client import EvernoteClient, NoteStore
from django.core.management.base import BaseCommand
import requests

from articles.models import Resources


class MyCommand(BaseCommand):
    # target_book = "key"  # subclass fill this field
    # local_type = Article # subclass fill this field
    evernote_token = settings.EVERNOTE_TOKEN

    client = EvernoteClient(token=evernote_token,
                            sandbox=False,
                            service_host='app.yinxiang.com')
    noteStore = client.get_note_store()
    userStore = client.get_user_store()
    user_info = userStore.getPublicUserInfo('tianjun_cpp')


    def handle(self, *args, **options):
        # check update time, collect articles need update
        local_articles_info = self.get_local_articles_updated_time()
        remote_articles = self.get_evernote_articles_updated_time()
        articles_need_update = []
        articles_need_create = []
        for article in remote_articles:
            if local_articles_info.get(article.guid, None):
                if local_articles_info[article.guid] < (article.updated / 1000):
                    articles_need_update.append(article)
            else:
                articles_need_create.append(article)
        self.update_articles(articles_need_update, "update")
        self.update_articles(articles_need_create, "create")
        self.stdout.write("SUCCESS!")


    def get_local_articles_updated_time(self):
        all_articles = self.local_type.objects.all()
        return {x.evernote_guid: long(time.mktime(x.updated.timetuple()))
                for x in all_articles}


    def get_evernote_articles_updated_time(self):
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
        return mylist.notes


    def update_articles(self, notes, update_type):
        raise NotImplementedError

    def mark_down(self, note_detail):
        """
        change the content from evernote into markdown texts
        :param content:
        :return: processed markdown text
        """
        # try to get resources filenames
        resource_dict = {}
        if note_detail.resources:
            for r in note_detail.resources:
                self.process_resource(r)
                hex_hash = ''.join(["%02X" % (ord(x)) for x in r.data.bodyHash]).lower()
                if r.attributes.fileName:
                    resource_dict[hex_hash] = r.attributes.fileName

        html_parser = HTMLParser.HTMLParser()
        note_content = html_parser.unescape(note_detail.content)
        pre_processed = re.search(r'<en-note>(.+)</en-note>', note_content)
        if not pre_processed:
            return ""

        post_process = pre_processed.groups()[0] \
            .replace('<div><br clear="none"/></div>', '\n') \
            .replace('<br clear="none"/>', '\n') \
            .replace('<div>', '') \
            .replace('</div>', '\n')
        # post_process = unicode(post_process, 'utf-8')


        def _get_filename(matched):
            original_hash = matched.group("hash")
            file_name = resource_dict.get(original_hash, original_hash)
            if matched.group("type") == "image":
                return '![' + file_name + '](http://ontheroad.qiniudn.com/blog/resources/' + file_name + '/w660)'
            else:
                return '[' + file_name + '](http://ontheroad.qiniudn.com/blog/resources/' + file_name + ')'

        md_str = re.sub(r'<en-media.+?hash="(?P<hash>\w+)" type="(?P<type>\w+)/.+?</en-media>',
                        _get_filename,
                        post_process)

        def _get_gist_link(matched):
            link = matched.group("link")
            try:
                resp = requests.get(link, timeout=10.0)
                result = resp.text
            except requests.exceptions.ReadTimeout, e:
                result = ""

            return '<script>' + result + '</script>'

        md_fillcode_str = re.sub(r'<script src="(?P<link>.+?)"></script>', _get_gist_link, md_str)

        return md_fillcode_str

    def process_resource(self, resource):
        hex_hash = ''.join(["%02X" % (ord(x)) for x in resource.data.bodyHash]).lower()
        file_name = resource.attributes.fileName
        evernote_guid = resource.guid

        resources = Resources.objects.filter(evernote_guid=evernote_guid)
        if not resources:
            r = Resources(hex_hash=hex_hash,
                          evernote_guid=evernote_guid,
                          file_name=file_name)
            r.save()

