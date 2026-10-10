import sys

import uvicorn
from fastapi import FastAPI
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sample.api.api import api_router
from sample.db.session import engine

app = FastAPI()

app.include_router(api_router)

SQLAlchemyInstrumentor().instrument(
    engine=engine.sync_engine, enable_commenter=True, commenter_options={}
)
PsycopgInstrumentor().instrument()

if __name__ == "__main__":
    # psycopg の非同期モードは Windows の ProactorEventLoop では動かないため、
    # Windows のみ SelectorEventLoop を使う
    loop = "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto"
    uvicorn.run(app, host="0.0.0.0", port=8000, loop=loop)
