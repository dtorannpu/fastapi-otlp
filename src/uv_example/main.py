import uvicorn
from fastapi import FastAPI
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sample.api.api import api_router

app = FastAPI()

app.include_router(api_router)

SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})
PsycopgInstrumentor().instrument()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
