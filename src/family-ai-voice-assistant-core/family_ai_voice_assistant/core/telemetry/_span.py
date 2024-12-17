from functools import wraps
from opentelemetry.trace import Status, StatusCode

from ._tracer_manager import TracerManager


def trace(
    log_io: bool = False,
    args_filter_callback: callable = None,
    kwargs_filter_callback: callable = None,
    ouput_filter_callback: callable = None,
    span_name: str = None
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_span_name = span_name or func.__name__
            with (
                TracerManager().tracer.start_as_current_span(current_span_name)
                as span
            ):
                span.set_attribute("function.name", func.__name__)

                if log_io:
                    if args_filter_callback:
                        filtered_args = args_filter_callback(args)
                    else:
                        filtered_args = args
                    span.set_attribute("input.args", str(filtered_args))
                    if kwargs_filter_callback:
                        filtered_kwargs = kwargs_filter_callback(kwargs)
                    else:
                        filtered_kwargs = kwargs
                    span.set_attribute("input.kwargs", str(filtered_kwargs))

                try:
                    result = func(*args, **kwargs)

                    if log_io:
                        if ouput_filter_callback:
                            filtered_result = ouput_filter_callback(result)
                        else:
                            filtered_result = result
                        span.set_attribute("output", str(filtered_result))

                    span.set_status(Status(StatusCode.OK))

                    return result
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        return wrapper
    return decorator
