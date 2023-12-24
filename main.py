import uvicorn
from fastapi import FastAPI
from app.routes import user_routes, event_routes, comment_routes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(event_routes.router)
app.include_router(comment_routes.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)

#
#
