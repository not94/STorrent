STorrent
---

A Simple library to create and parse torrent


Support
---
Python 3.6

Deploy
---
```angular2html
pip install -r requirements.txt
```


Demo
---

create torrent in current directory.
```python
from torrent.torrent import Torrent
t = Torrent("demo", ["http://121.14.98.151:9090/announce"])
t.create()
```

parse torrent.
```python
from torrent.parser import TorrentParser
parser = TorrentParser("demo/anime.torrent")

# show torrent trackers
print(parser.announce)

# show torrent file info
print(parser.file_info)
```

If you have any questions, welcome to ask me for help.
