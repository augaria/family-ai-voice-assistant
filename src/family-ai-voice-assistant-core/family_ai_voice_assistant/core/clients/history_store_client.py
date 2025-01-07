from abc import ABC, abstractmethod
from typing import List, Tuple

from ..contracts import ChatRecord, SerilizableChatRecord
from .file_store_client import FileStoreClient
from .client_manager import ClientManager
from ..configs import ConfigManager, HistoryStoreConfig
from ..helpers.mongodb_manager import MongoDbManager
from ..telemetry import trace
from ..logging import Loggers


class HistoryStoreClient(ABC):
    """
    Manages storage of chat history records.
    """

    @trace()
    def save(self, records: List[ChatRecord]):
        """
        Save the chat records to storage.

        :param records: The list of chat records to save.
        """

        serializable_records = []
        file_store_client = ClientManager().get_client(FileStoreClient)

        for record in records:
            serializable_record, wav_record = self._generate_stored_data(
                record
            )
            if serializable_record is not None:
                serializable_records.append(serializable_record)
            if wav_record is not None and file_store_client is not None:
                try:
                    file_store_client.save_to(wav_record[0], wav_record[1])
                except Exception as e:
                    Loggers().history_store.error(
                        f"Failed to save wav file: {str(e)}"
                    )

        self._save_serilizable_records(serializable_records)
        Loggers().history_store.info(
            "History records saved successfully. "
            f"Total count : {len(serializable_records)}"
        )

    def _generate_stored_data(
        self,
        record: ChatRecord
    ) -> Tuple[SerilizableChatRecord, Tuple[str, bytes]]:
        """
        Generate data for storage from a chat record.

        :param record: The chat record to process.
        :return: A tuple of serializable chat record and wav file data.
        """

        serializable_record = None
        wav_record = None
        wav_file_path = None

        if record.wav_bytes is not None:
            year_month = record.timestamp.strftime('%Y_%m')
            wav_file_path = (
                f"/chatbot/audio/{year_month}"
                f"/{record.timestamp.strftime('%Y%m%d_%H%M%S')}.wav"
            )
            wav_record = (wav_file_path, record.wav_bytes)

        if not record.serilizable:
            return serializable_record, wav_record

        additional_properties = {
            k: v
            for k, v in record.message.items()
            if k not in {'role', 'name', 'content'}
        }

        serializable_record = SerilizableChatRecord(
            session_id=record.session_id,
            role=record.message['role'],
            name=record.message.get('name', None),
            message_content=record.message.get('content', None),
            timestamp=record.timestamp.isoformat(),
            wav_file_path=wav_file_path,
            additional_properties=additional_properties
        )
        return serializable_record, wav_record

    @abstractmethod
    def _save_serilizable_records(self,  records: List[SerilizableChatRecord]):
        """
        Save serializable chat records.

        :param records: The list of serializable chat records to save.
        """
        pass


class MongoHistoryStore(HistoryStoreClient):

    def __init__(self):
        config = ConfigManager().get_instance(HistoryStoreConfig)
        if config is None or config.connection_str is None:
            raise ValueError("History store config is not valid")
        self._client = MongoDbManager().get_instance(config.connection_str)
        self._db = self._client[config.database_name]
        self._collection = self._db[config.collection_name]

    def _save_serilizable_records(self,  records: List[SerilizableChatRecord]):
        mongo_records = [record.to_dict() for record in records]
        self._collection.insert_many(mongo_records)
