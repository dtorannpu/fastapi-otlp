import uvicorn
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from sample.api.api import api_router


def instrument(application: FastAPI):
    resource = Resource.create(
        {
            SERVICE_NAME: "fastapi-otlp",
            SERVICE_INSTANCE_ID: "fastapi-otlp",
        }
    )

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)
    FastAPIInstrumentor.instrument_app(application)

    SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})

    Psycopg2Instrumentor().instrument()


app = FastAPI()

app.include_router(api_router)

instrument(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
