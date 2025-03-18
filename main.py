from fastapi import FastAPI
from routers import inserate, inserat
import os

app = FastAPI(
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Kleinanzeigen API",
        "endpoints": [
            "/inserate",
            "/inserat/{id}"
        ]
    }

app.include_router(inserate.router)
app.include_router(inserat.router)

# Für den Render.com-Deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False) 