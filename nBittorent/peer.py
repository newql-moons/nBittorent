import socket
import struct


class Peer(object):
    def __init__(self, addr, info_hash, self_id):
        self.__hash = info_hash

        self.am_chocking = 1
        self.am_interested = 0
        self.peer_chocking = 1
        self.peer_interested = 0

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect(addr)
        print(self.shake_hand(self_id))

    def shake_hand(self, self_id):
        data = struct.pack('!B', 19)
        data += b'BitTorrent protocol'
        data += b'\x00\x00\x00\x00\x00\x00\x00\x00'
        data += self.__hash
        data += self_id
        self.__sock.send(data)

        resp = self.__sock.recv(68)
        pstrlen = struct.unpack('!B', resp[0])[0]
        pstr = resp[1: pstrlen + 1]
        reserved = resp[pstrlen + 1: pstrlen + 9]
        info_hash = resp[pstrlen + 9:]

        return pstrlen, pstr, reserved, info_hash

    def close(self):
        self.__sock.close()
