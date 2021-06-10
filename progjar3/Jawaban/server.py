from socket import *
import socket
import threading
import logging
import time
import sys
from library import *
import random

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.buffername = random.randint(65,90)
        self.buffername = 'buffer_' + chr(self.buffername)
        self.nama = 'server_'
        self.check = 0
        print('connection started')
        threading.Thread.__init__(self)

    def run(self):
        time_start = datetime.datetime.now()
        while True:
            try:
                incoming = self.connection.recv(32)
                print(incoming)
                endcheck = incoming
                endcheck = endcheck[-3:]
                if endcheck == b'end' or endcheck == b'':
                    fp = open(self.buffername, 'ab')
                    fp.write(incoming[:-3])
                    fp.close()

                    print(self.buffername,'with',self.nama)
                    os.rename(self.buffername,self.nama)
                    time_end = datetime.datetime.now()
                    process_time = time_end - time_start
                    logging.warning(f'File {self.nama} Dimulai:{time_start} selesai:{time_end} Lama:{process_time}')
                    return

                elif(self.check == 0):
                    try:
                        file_information = incoming.decode().split(" ")
                        self.nama += file_information[0].strip()
                        # print(self.nama)
                        self.check = 1
                    except Exception as e:
                        print(repr(e))

                fp = open(self.buffername,'ab')
                fp.write(incoming)
                fp.close()
            except Exception as e:
                print(repr(e))
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('127.0.0.1', 8989))
        self.my_socket.listen(10)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()

