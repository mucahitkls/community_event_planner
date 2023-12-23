from fastapi import FastAPI
from app.routes import user_routes, event_routes, comment_routes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(event_routes.router)
app.include_router(comment_routes.router)