from nBittorent.tracker import UDPTracker
from nBittorent.torrent import Torrent
import random


if __name__ == '__main__':
    torrent = Torrent('4F9321E31848F7C4618A6477C42CFEB504B1E6A3.torrent')
    peer_id = b'asjdhfiashdfashdfais'
    tracker = UDPTracker('tracker.opentrackr.org', 1337)
    peers = tracker.announce(torrent.info_hash(), peer_id, 0, 0, 0, UDPTracker.event.none, 0, random.getrandbits(32),
                             -1, 7777)
    print(peers)
    print(len(peers))
