from abc import ABC, abstractmethod
import requests
import os

from ..config import ConfigManager, FileStoreConfig
from ..telemetry import trace
from ..logging import Loggers


class FileStoreClient(ABC):

    @property
    def destination(self) -> str:
        return ConfigManager().get_instance(FileStoreConfig).destination

    @abstractmethod
    def save_to(self, relative_path: str, data: bytes):
        pass


class LocalFileStore(FileStoreClient):

    @trace()
    def save_to(self, relative_path: str, data: bytes):
        full_path = f"{self.destination}/{relative_path}"
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full_path, 'wb') as f:
            f.write(data)
        Loggers().file_store.info(f"File saved successfully at {full_path}")


class RestFileStore(FileStoreClient):

    @trace()
    def save_to(self, relative_path: str, data: bytes):
        response = requests.post(
            self.destination,
            files={relative_path: data},
        )
        if response.status_code == 200:
            Loggers().file_store.info(
                f"File {relative_path} saved through {self.destination}"
            )
        else:
            error_message = (
                f"Failed to save file {relative_path} "
                f"through {self.destination}, "
                f"status code: {response.status_code}, "
                f"response: {response.text}"
            )
            raise Exception(error_message)
