# -*- coding:utf-8 -*-
import os
import time
import io
import hashlib
import bencoder

from torrent.utils import FileHandler, DirectoryHandler
from torrent.decorator import cached_property


class Torrent(object):

    PIECES_256K = 2 ** 18
    PIECES_1M = 2 ** 20
    PIECES_SIZE = [PIECES_256K, PIECES_1M]

    def __init__(self, path, trackers, name=None, created_by=None, encoding='UTF-8',
                 piece_length=None, use_hash_tree=False):
        self.path = path
        self.trackers = trackers
        self.created_by = created_by
        self.encoding = encoding
        self.name = name
        self.use_hash_tree = use_hash_tree
        self._piece_length = piece_length

    @property
    def announce(self):
        return self.trackers[0]

    @property
    def announce_list(self):
        return [[t] for t in self.trackers] if len(self.trackers) > 1 else []

    @cached_property
    def creation_date(self):
        return int(time.time())

    @cached_property
    def handler(self):
        if os.path.isfile(self.path):
            return FileHandler(self.path)
        elif os.path.isdir(self.path):
            return DirectoryHandler(self.path)

    @property
    def piece_length(self):
        if self._piece_length is None:
            self._piece_length = self.PIECES_1M
        return self._piece_length

    @cached_property
    def pieces(self):
        fd = io.BytesIO(self.handler.get_data())
        hasher = hashlib.sha1()
        pieces = bytearray()
        while True:
            to_hash_bytes = fd.read(self.piece_length)
            if not to_hash_bytes:
                break
            hasher.update(to_hash_bytes)
            pieces += hasher.digest()
        return bytes(pieces)

    @property
    def root_hash(self):
        pass

    @cached_property
    def info(self):
        info_dict = self.handler.file_info.copy()
        if self.name is not None:
            info_dict['name'] = self.name
        info_dict['piece length'] = self.piece_length
        if self.use_hash_tree:
            info_dict['root hash'] = self.root_hash
        else:
            info_dict['pieces'] = self.pieces

        return info_dict

    def validate(self):
        if self.piece_length not in self.PIECES_SIZE:
            raise ValueError('Illegal piece length')

    def create(self, target_path=None):
        self.validate()
        if not target_path:
            target_path = os.getcwd()
        torrent_info = {
            "announce": self.announce,
            "creation date": self.creation_date,
            "encoding": self.encoding,
            "info": self.info
        }
        if self.announce_list:
            torrent_info['announce-list'] = self.announce_list
        if self.created_by:
            torrent_info['created by'] = self.created_by

        encode_info = bencoder.bencode(torrent_info)
        file_name = os.path.join(target_path, self.info['name'] + ".torrent")
        with open(file_name, "wb") as f:
            f.write(encode_info)
