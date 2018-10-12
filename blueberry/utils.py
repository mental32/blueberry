import sys
import time
import socket

_timelog_stdout = sys.stdout

def timelog(msg):
    timestamp = int(time.time())
    _timelog_stdout.write('[%s] %s\n' % (timestamp, msg))
    _timelog_stdout.flush()
    return timestamp

def get_local_addr():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    addr = sock.getsockname()[0]
    sock.close()
    return addr

def wait_for_connection(timeout=None):
    sock = socket.socket()
    start = int(time.time())

    while True:
        if timeout and int(time.time()) >= start + timeout:
            raise TimeoutError

        try:
            sock.connect(('8.8.8.8', 53))
            return sock.close()
        except OSError:
            time.sleep(0.5)
        continue

def check_inet_connectivity():
    sock = socket.socket()
    try:
        sock.connect(('8.8.8.8', 53))
        sock.close()
    except OSError:
        return False
    else:
        return True
