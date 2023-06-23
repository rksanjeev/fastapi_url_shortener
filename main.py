from fastapi import FastAPI
from url_shortener import  url_shorterner_router
app = FastAPI()

app.include_router(url_shorterner_router)
