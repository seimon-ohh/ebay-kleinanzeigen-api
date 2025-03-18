from fastapi import FastAPI
from routers import inserate, inserat
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    version="1.0.0"
)

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt alle Origins
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle Methoden
    allow_headers=["*"],  # Erlaubt alle Header
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Kleinanzeigen API",
        "endpoints": [
            "/inserate",
            "/inserat/{id}",
            "/find"  # Falls dieser Endpunkt existieren soll
        ]
    }

app.include_router(inserate.router)
app.include_router(inserat.router)

# Alias für /inserate als /find (falls dies benötigt wird)
@app.get("/find")
async def find_alias(query: str = None, location: str = None, radius: int = None, 
                    min_price: int = None, max_price: int = None, page_count: int = 1):
    # Verwendet direkt die get_inserate Funktion aus dem inserate Router
    return await inserate.get_inserate(query, location, radius, min_price, max_price, page_count)

# Für den Render.com-Deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False) 