from dataclasses import dataclass
import enum

from .config import Config


class TelemetryExporterType(str, enum.Enum):
    CONSOLE = 'console'
    GRPC = 'grpc'
    HTTP = 'http'


@dataclass
class TelemetryConfig(Config):
    exporter_type: TelemetryExporterType = TelemetryExporterType.CONSOLE
    endpoint: str = None
