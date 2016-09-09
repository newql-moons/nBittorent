from .utils import bencode
from hashlib import sha1


class Torrent(object):
    def __init__(self, path):
        with open(path, 'rb') as fp:
            s = fp.read()
        self.__meta = bencode.loads(s)

    def info_hash(self, hex_str=False):
        info = self.__meta[b'info']
        h = sha1(bencode.dumps(info))
        if hex_str:
            return h.hexdigest()
        else:
            return h.digest()
