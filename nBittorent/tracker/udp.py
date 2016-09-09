import struct
import socket
import random


class UDPTracker(object):
    class action(object):
        connect = 0
        announce = 1
        scrape = 2
        error = 3

    class event(object):
        """0: none; 1: completed; 2: started; 3: stopped"""
        none = 0
        completed = 1
        started = 2
        stopped = 3

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.connection_id = self.connect()

    def request(self, connection_id, action, data):
        transaction_id = random.getrandbits(32)

        package = struct.pack('!QII', connection_id, action, transaction_id)
        package += data

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(package, (self.__host, self.__port,))
        resp, addr = sock.recvfrom(1024)

        a, t = struct.unpack('!II', resp[:8])
        if a != action:
            raise Exception('The action is not equal to the one you chose.')
        if t != transaction_id:
            raise Exception('The transaction ID is not equal to the one you chose.')
        sock.close()

        return resp[8:]

    def connect(self):
        resp = self.request(0x41727101980, self.action.connect, b'')
        connection_id = struct.unpack('!Q', resp)[0]
        return connection_id

    def announce(self, info_hash, peer_id, downloaded, left,
                 uploaded, event, ip, key, num_want, port):
        data = b''
        data += info_hash
        data += peer_id
        data += struct.pack('!QQQ', downloaded, left, uploaded)
        data += struct.pack('!IIIi', event, ip, key, num_want)
        data += struct.pack('!H', port)

        resp = self.request(self.connection_id, self.action.announce, data)
        interval, leechers, seeders = struct.unpack('!III', resp[:12])
        peers_num = leechers + seeders
        peers = []
        for i in range(peers_num):
            ip, port = struct.unpack('IH', resp[12 + i * 6: 12 + (i + 1) * 6])
            peers.append((socket.inet_ntoa(struct.pack('I',socket.htonl(ip))), port))
        return peers
