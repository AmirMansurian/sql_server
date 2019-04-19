import socket

def main ():

    host = '127.0.0.1'
    port = 12345

    s=socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((host, port))

    while True :

        msg = input('client > ')
        s.send (msg.encode('utf-8'))
        data = s.recv(2048)
        print ('server >  ', data.decode('utf-8'))

    s.close ()

if __name__ == '__main__':
    main()