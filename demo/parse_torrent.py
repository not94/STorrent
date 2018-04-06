# -*- coding:utf-8 -*-
from torrent.parser import TorrentParser

if __name__ == '__main__':
    parser = TorrentParser("demo/anime.torrent")

    # show torrent trackers
    print(parser.announce)

    # show torrent file info
    print(parser.file_info)
