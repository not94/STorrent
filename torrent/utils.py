# -*- coding:utf-8 -*-
import os

from abc import ABCMeta, abstractmethod

from torrent.decorator import cached_property


class DataHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path

    @property
    def file_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_data(self):
        raise NotImplementedError


class FileHandler(DataHandler):

    def __init__(self, path):
        super(FileHandler, self).__init__(path)
        self._content = None

    @cached_property
    def file_info(self):
        return {
            "name": os.path.basename(self.path),
            "length": self.get_size()
        }

    def get_data(self, reload=False):
        if self._content is None or reload:
            with open(self.path, "rb") as fd:
                self._content = fd.read()
        return self._content

    def get_size(self):
        return os.path.getsize(self.path)


class TorrentFileHandler(FileHandler):

    @staticmethod
    def utf_8_to_unicode(obj):
        func = TorrentFileHandler.utf_8_to_unicode
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        if isinstance(obj, list):
            return [func(item) for item in obj]
        if isinstance(obj, dict):
            # special for info pieces hash
            d = {}
            for k, v in obj.items():
                decode_key = func(k)
                if decode_key != "pieces":
                    d[decode_key] = func(v)
                else:
                    d[decode_key] = v
            return d
        return obj


class DirectoryHandler(DataHandler):

    @cached_property
    def file_paths(self):
        file_paths = []
        # 可以考虑做一个pattern过滤
        for root, dirs, files in os.walk(self.path):
            files = [f for f in files if not f[0] == '0']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for f in files:
                file_paths.append(os.path.join(root, f))
        return file_paths

    @cached_property
    def file_info(self):
        files = []
        for file_path in self.file_paths:
            rel_path = os.path.relpath(file_path, self.path)
            files.append({
                "length": os.path.getsize(file_path),
                "path": os.path.normpath(rel_path).split(os.sep)
            })
        path = self.path[:-1] if self.path.endswith('/') else self.path
        return {
            "name": os.path.basename(path),
            "files": files
        }

    def get_data(self):
        all_file_bytes = bytearray()
        for file_path in self.file_paths:
            with open(file_path, "rb") as f:
                all_file_bytes += f.read()
        return all_file_bytes


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
