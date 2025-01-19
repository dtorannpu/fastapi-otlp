import uvicorn
from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry import trace

from sample.api.api import api_router


def instrument(application: FastAPI):
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: "uv-example",
        ResourceAttributes.SERVICE_INSTANCE_ID: "uv-example"
    })

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(application)


app = FastAPI()

app.include_router(api_router)

instrument(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
