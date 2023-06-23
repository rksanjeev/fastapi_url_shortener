from .router import router as url_shorterner_router
import url_shortener.models
from db import engine

models.Base.metadata.create_all(bind=engine)