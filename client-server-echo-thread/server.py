import socket
from _thread import *
import threading

print_lock = threading.Lock()


def tabe(c):
    while True:
        data = c.recv(2048)
        c.send(data)
    c.close()


def main():
    host = ''
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    while True:
        c, adder = s.accept()

        print_lock.acquire()

        start_new_thread(tabe, (c,))

    s.close()

if __name__ == '__main__':
    main()