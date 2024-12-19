from ctypes import *  # noqa: F403
from contextlib import contextmanager
from functools import wraps


def py_error_handler(filename, line, function, err, fmt):
    pass


ERROR_HANDLER_FUNC = CFUNCTYPE(  # noqa: F405
    None, c_char_p, c_int, c_char_p, c_int, c_char_p  # noqa: F405
)

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def no_alsa_context():
    try:
        asound = cdll.LoadLibrary('libasound.so')  # noqa: F405
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except Exception:
        yield
        pass


def no_alsa_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with no_alsa_context():
            return func(*args, **kwargs)
    return wrapper
