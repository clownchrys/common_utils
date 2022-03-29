from typing import Any
import socket


def is_exception(obj: Any) -> bool:
    return issubclass(type(obj), BaseException)


def is_iterable(obj: Any) -> bool:
    try:
        iter(obj)
    except:
        return False
    else:
        return True
    

def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('10.255.255.255', 1))  # doesn't even have to be reachable
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()

    return IP
