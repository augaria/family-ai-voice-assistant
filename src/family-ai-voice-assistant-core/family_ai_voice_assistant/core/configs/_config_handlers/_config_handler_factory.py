import threading

from ._yaml_config_handler import _YamlConfigHandler


class _ConfigHandlerFactory:
    _yaml_config_path = None
    _instance_lock = threading.Lock()
    _instance = None

    @staticmethod
    def set_yaml_config_path(path: str):
        _ConfigHandlerFactory._yaml_config_path = path

    @staticmethod
    def get_instance():
        if _ConfigHandlerFactory._instance is None:
            with _ConfigHandlerFactory._instance_lock:
                if _ConfigHandlerFactory._instance is None:
                    if _ConfigHandlerFactory._yaml_config_path:
                        _ConfigHandlerFactory._instance = _YamlConfigHandler(
                            _ConfigHandlerFactory._yaml_config_path
                        )
                    else:
                        _ConfigHandlerFactory._instance = None
        return _ConfigHandlerFactory._instance
