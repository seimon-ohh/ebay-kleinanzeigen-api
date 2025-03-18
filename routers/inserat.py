from scrapers.inserat import get_inserate_details
from fastapi import APIRouter, HTTPException
from utils.browser import PlaywrightManager

router = APIRouter()

@router.get("/inserat/{id}")
async def get_inserat(id: str):
    browser_manager = PlaywrightManager()
    await browser_manager.start()
    try:
        page = await browser_manager.new_context_page()
        try:
            # Verwende die klarere URL-Form (ohne 's-anzeige') für bessere Kompatibilität
            url = f"https://www.kleinanzeigen.de/s-anzeige/{id}"
            result = await get_inserate_details(url, page)
            return {"success": True, "data": result}
        except Exception as e:
            # Bei Fehler versuche einen alternativen URL-Muster
            alternative_url = f"https://www.kleinanzeigen.de/anzeigen/{id}"
            try:
                result = await get_inserate_details(alternative_url, page)
                return {"success": True, "data": result}
            except Exception as inner_e:
                raise HTTPException(status_code=404, detail=f"Inserat mit ID {id} nicht gefunden: {str(inner_e)}")
        finally:
            await browser_manager.close_page(page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen des Inserats: {str(e)}")
    finally:
        await browser_manager.close() 