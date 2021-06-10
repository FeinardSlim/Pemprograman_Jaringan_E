from socket import *
import socket
import multiprocessing
import logging
import time
import sys
from library import *
import random

def handle(self, connection, address ,buffername,filename):
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger("process-%r" % (address,))
    self.connection = connection
    self.address = address
    self.check = 0
    time_start = datetime.datetime.now()
    while True:
        try:
            incoming = self.connection.recv(32)
            # print(incoming)
            # time.sleep(0.001)
            endcheck = incoming
            endcheck = endcheck[-3:]
            if endcheck == b'end' or endcheck == b'':
                fp = open(buffername, 'ab')
                fp.write(incoming[:-3])
                fp.close()

                print(buffername, 'with', filename)
                name = 'server_' + filename.decode()
                os.rename(buffername,name)
                time_end = datetime.datetime.now()
                process_time = time_end - time_start
                return

            elif incoming == "":
                logger.debug("Socket closed remotely")
                break

            fp = open(buffername, 'ab')
            fp.write(incoming)
            fp.close()
        except Exception as e:
            print(repr(e))

    self.connection.close()


class Server():
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.my_socket.bind(('', 8989))
        self.my_socket.listen(10)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            try:
                self.filename = self.connection.recv(32)
                self.buffername = random.randint(65, 90)
                self.buffername = 'buffer_' + chr(self.buffername)
                clt = multiprocessing.Process(target=handle, args=(self, self.connection, self.client_address,self.buffername,self.filename))
                # clt.daemon = True
                self.the_clients.append(clt)
                clt.start()
            except:
                print('error')
                self.connection.close()

def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()

