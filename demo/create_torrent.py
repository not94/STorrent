# -*- coding:utf-8 -*-
from torrent.torrent import Torrent

t = Torrent("demo", ["http://121.14.98.151:9090/announce"])
t.create()