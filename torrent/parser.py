# -*- coding:utf-8 -*-
import bencoder
import itertools
import hashlib

from torrent.utils import TorrentFileHandler, chunks
from torrent.decorator import cached_property


class TorrentParser(object):

    def __init__(self, torrent_path):
        self.path = torrent_path
        self.handler = TorrentFileHandler(self.path)

    @property
    def torrent_size(self):
        return "{} KB".format(self.handler.get_size() / 1024)

    @cached_property
    def meta_info(self):
        encode_info = bencoder.bdecode(self.handler.get_data())
        return self.handler.utf_8_to_unicode(encode_info)

    @property
    def announce(self):
        """
        the url of the tracker
        :return:
        """
        return self.meta_info['announce']

    @property
    def announces_list(self):
        """
        refer to BEP 12
        :return:
        """
        return list(itertools.chain(*self.meta_info.get('announce-list', [])))

    @property
    def creation_date(self):
        return self.meta_info.get('creation date', "")

    @property
    def comment(self):
        return self.meta_info.get("comment", "")

    @property
    def created_by(self):
        return self.meta_info.get("create by", "")

    @property
    def encoding(self):
        return self.meta_info.get("encoding", "")

    @cached_property
    def info(self):
        return self.meta_info['info']

    @property
    def piece_length(self):
        return self.info.get("piece length")

    @cached_property
    def file_info(self):
        if self.info.get('length'):
            return {
                "file_name": self.info.get('name'),
                "length": self.info.get('length'),
            }
        else:
            return {
                "directory_name": self.info.get('name'),
                "files": self.info.get('files')
            }

    @cached_property
    def pieces(self):
        return list(chunks(self.info.get('pieces'), 20))

    @cached_property
    def info_hash(self):
        raw_info = bencoder.bdecode(self.handler.get_data()).get(b'info')
        return hashlib.sha1(bencoder.bencode(raw_info)).hexdigest()

    def show_pieces_length(self, MB=False, KB=False):
        if MB:
            return "{} MB".format(self.piece_length / 1024 / 1024)
        if KB:
            return "{} KB".format(self.piece_length / 1024)
        return "{} B".format(self.piece_length)