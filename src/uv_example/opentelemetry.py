from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider


def initialize_tracer_provider():
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
