from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.api import items, orders
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Order Management")

app.include_router(items.router)
app.include_router(orders.router)


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )