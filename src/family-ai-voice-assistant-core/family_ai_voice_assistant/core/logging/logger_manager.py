import logging
from ..contracts import LoggerName
from ..utils.global_instance_manager import GlobalInstanceManager
from ._ai_assistant_logger import AIAssistantLogger


logging.setLoggerClass(AIAssistantLogger)


class LoggerManager(GlobalInstanceManager):

    def get_instance(
        self,
        logger_name: LoggerName
    ) -> logging.Logger:
        return super()._get_instance(
            identifier=logger_name,
            logger_name=logger_name
        )

    def _create_instance(self, logger_name: LoggerName) -> logging.Logger:
        return logging.getLogger(logger_name.value)
