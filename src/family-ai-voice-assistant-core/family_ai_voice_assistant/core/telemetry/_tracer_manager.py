from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporter_grpc
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporter_http
)

from ..utils.singleton_meta import SingletonMeta
from ..configs import TelemetryConfig, ConfigManager, TelemetryExporterType


service_name = "family_ai_voice_assistant"


class TracerManager(metaclass=SingletonMeta):

    def __init__(self):

        resource = Resource.create(attributes={
            "service.name": service_name
        })
        provider = TracerProvider(resource=resource)

        config = ConfigManager().get_instance(TelemetryConfig)
        if config is None:
            exporter = SpanExporter()
        elif config.exporter_type == TelemetryExporterType.GRPC:
            exporter = OTLPSpanExporter_grpc(
                endpoint=config.endpoint,
                insecure=True
            )
        elif config.exporter_type == TelemetryExporterType.HTTP:
            exporter = OTLPSpanExporter_http(
                endpoint=config.endpoint,
                insecure=True
            )
        elif config.exporter_type == TelemetryExporterType.CONSOLE:
            exporter = ConsoleSpanExporter()
        else:
            raise ValueError(
                f"Invalid telemetry exporter type {config.exporter_type}"
            )

        self._span_processor = BatchSpanProcessor(exporter)

        provider.add_span_processor(self._span_processor)
        trace.set_tracer_provider(provider)
        self._tracer = trace.get_tracer(service_name)

    @property
    def tracer(self):
        return self._tracer

    def shutdown(self):
        self._span_processor.shutdown()
