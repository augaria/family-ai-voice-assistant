from abc import ABC, abstractmethod
import requests
import os
import argparse

from flask import Flask, jsonify, request

from ..configs import ConfigManager, FileStoreConfig
from ..telemetry import trace
from ..logging import Loggers


class FileStoreClient(ABC):
    """
    Abstract base class for a file storage client.
    """

    @property
    def destination(self) -> str:
        """
        Get the destination path for file storage.
        """
        return ConfigManager().get_instance(FileStoreConfig).destination

    @abstractmethod
    def save_to(self, relative_path: str, data: bytes):
        """
        Save data to the specified relative path.

        :param relative_path: The relative path where data should be saved.
        :param data: The data to save.
        """
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


class RestFileStoreServer:
    def __init__(self, files_root: str, port: int):
        self._app = Flask(__name__)
        self.setup_routes()
        self.files_root = files_root
        self.port = port

    def setup_routes(self):
        @self._app.route('/health', methods=['GET'])
        def health_check():
            return jsonify(status="UP"), 200

        @self._app.route('/files/upload', methods=['POST'])
        def upload_file():
            try:
                for new_filename, file in request.files.items():
                    destination = f"{self.files_root}/{new_filename}"
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    file.save(destination)
                return 'File uploaded successfully', 200
            except Exception as e:
                return str(e), 500

    def run(self):
        self._app.run(
            host='0.0.0.0',
            port=self.port,
            debug=False
        )


def start_file_server():
    parser = argparse.ArgumentParser(description='File Server')
    parser.add_argument(
        '--root',
        type=str,
        required=True,
        help='Root directory for file storage'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5100,
        help='Port to run the server on'
    )
    args = parser.parse_args()
    server = RestFileStoreServer(args.root, args.port)
    server.run()
