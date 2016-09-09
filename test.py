from nBittorent.tracker import UDPTracker
from nBittorent.torrent import Torrent
import random


if __name__ == '__main__':
    torrent = Torrent('FF003D59075ECFA82DCF9B5BD2C4DA133B7AD7A1.torrent')
    peer_id = b'asjdhfiashdfashdfais'
    tracker = UDPTracker('tracker.opentrackr.org', 1337)
    print(tracker.connect())
    peers = tracker.announce(torrent.info_hash(), peer_id, 0, 0, 0, UDPTracker.event.none, 0, random.getrandbits(32), -1, 7777)
    print(peers)
    print(len(peers))
