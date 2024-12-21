from pymongo import MongoClient

from ..utils.global_instance_manager import GlobalInstanceManager


class MongoDbManager(GlobalInstanceManager):

    def get_instance(
        self,
        connection_string: str
    ) -> MongoClient:
        return super()._get_instance(
            identifier=connection_string,
            connection_string=connection_string
        )

    def _create_instance(self, connection_string: str) -> MongoClient:
        return MongoClient(connection_string)
