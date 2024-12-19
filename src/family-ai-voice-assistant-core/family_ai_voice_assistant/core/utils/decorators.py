import signal
from typing import List
import concurrent.futures
import threading

from ..clients.waker_client import WakerClient


def timeout(seconds):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("Function timed out")

        def wrapped(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, signal.SIG_DFL)

            return result

        return wrapped

    return decorator


def handler(signum, frame):
    print("Function is Interrupted")
    raise InterruptedError("Function is Interrupted")


def interrupt(wakers: List[WakerClient]):
    if not wakers:
        return
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = [executor.submit(waker.wake) for waker in wakers]
        concurrent.futures.wait(
            tasks, return_when=concurrent.futures.ALL_COMPLETED)
    print("before signal")
    signal.alarm(1)
    print("after signal")


def interrupt_by_wakers(wakers: List[WakerClient]):
    def decorator(func):

        def wrapped(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)

            try:
                thread = threading.Thread(target=interrupt, args=(wakers,))
                thread.start()
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, signal.SIG_DFL)
                WakerClient.is_waiting = False
                thread.join()

            return result

        return wrapped

    return decorator
