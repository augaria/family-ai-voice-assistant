import threading


class SingletonMeta(type):
    def __init__(cls, name, bases, attrs):
        cls._instance = None
        cls._singletonmeta_lock = threading.Lock()
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._singletonmeta_lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
