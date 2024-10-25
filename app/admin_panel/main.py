from fastapi import FastAPI

from .core.config import settings


app = FastAPI(
    title=settings.app_title,
    docs_url=settings.app_doc_url,
    redoc_url=None,
)


@app.get('/')
def read_root():
    return {'Hello': 'FastAPI'}