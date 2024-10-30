import socket
import hashlib
import threading
import multiprocessing
import logging

IP = '127.0.0.1'
PORT = 8080
LENGTH_P = 8
BUFFER_SIZE = 2048
ENCODED = ''
CPUS = multiprocessing.cpu_count()

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger = logging.getLogger(__name__)
logging.basicConfig(filename='md5logs.log', level=logging.DEBUG)


def md5_check(ranges, num):
    global ENCODED
    srange, erange = map(int, ranges[num - 1])
    logger.debug(ranges)
    print(srange, erange)
    for i in range(srange, erange + 1):
        res = hashlib.md5(str(i).encode()).hexdigest()
        if res == ENCODED:
            my_socket.send('Y#'.encode())
            my_socket.send((str(i) + '#').encode())
    my_socket.send('N#'.encode())


def main():
    ranges = []
    global ENCODED
    print('Connecting...')
    try:
        my_socket.connect((IP, PORT))
        ENCODED = my_socket.recv(BUFFER_SIZE).decode()
        my_socket.send(str(CPUS).encode())
        srange, erange = map(int, my_socket.recv(BUFFER_SIZE).decode().split('-'))  # get range in s-e format
        amount = (erange - srange) / CPUS  # divide end by number of cores available
        logger.debug(erange)
        erange = srange + amount
        logger.debug(amount)
        logger.debug(ranges)
        logger.debug(srange)
        for i in range(1, CPUS + 1):
            ranges.append((srange, erange))
            srange += amount
            erange += amount
        for i in range(0, CPUS + 1):
            thread = threading.Thread(target=md5_check(ranges, i))
            thread.start()
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    main()
