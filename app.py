from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import Response

from database.connect import db_session
from api.countries import router as countries_router
from api.products import router as products_router
from api.clusters import router as clusters_router

app = FastAPI()

routers = {
    'countries': countries_router,
    'clusters': clusters_router,
    'products': products_router,
}


def include_router(api, key):
    api.include_router(
        routers[key],
        prefix='/' + '_'.join(key.split()),
        tags=[key]
    )
    return api


for router in routers.keys():
    include_router(app, router)


@app.middleware('http')
async def db_session_middleware(request: Request, call_next: Callable) -> Response:
    try:
        request.state.db = next(db_session())
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
