from fastapi import HTTPException
from libs.websites import kleinanzeigen as lib
import re
import asyncio


async def get_inserate_details(url: str, page):
    try:
        # Optimierte Navigation und Timeouts
        await page.goto(url, timeout=45000)
        await page.wait_for_load_state("domcontentloaded", timeout=30000)

        # Optimiertes Warten auf wichtige Elemente
        try:
            await page.wait_for_selector("#viewad-title, .vap-title", state="visible", timeout=5000)
        except:
            print(f"[WARNING] Title element did not appear within 5 seconds for URL: {url}")
            # Versuche mit einer Pause, die Seite hat vielleicht verzögerte Ladezeiten
            await asyncio.sleep(2)

        # Weniger aggressives Scraping mit Fehlerbehandlung für jedes Element
        try:
            ad_id = await lib.get_element_content(page, "#viewad-ad-id-box > ul > li:nth-child(2)",
                                                default="")
            if not ad_id:
                # Alternative Methode für die ID
                match = re.search(r'/(\d+)$', url)
                ad_id = match.group(1) if match else "[ERROR] Ad ID not found"
        except:
            ad_id = "[ERROR] Ad ID not found"

        try:
            categories = [cat.strip() for cat in await lib.get_elements_content(page, ".breadcrump-link") if cat.strip()]
        except:
            categories = []

        try:
            title = await lib.get_element_content(page, "#viewad-title, .vap-title", default="[ERROR] Title not found")
        except:
            title = "[ERROR] Title not found"

        try:
            price_element = await lib.get_element_content(page, "#viewad-price, .vap-price")
            price = lib.parse_price(price_element)
        except:
            price = ""

        try:
            views = await lib.get_element_content(page, "#viewad-cntr-num")
        except:
            views = "0"

        try:
            description = await lib.get_element_content(page, "#viewad-description-text, .vap-description")
            if description:
                description = re.sub(r'[ \t]+', ' ', description).strip()
                description = re.sub(r'\n+', '\n', description)
        except:
            description = ""

        # Asynchron mehrere Elemente parallel scrapen
        images, seller_details, details, features, shipping, location, extra_info = await asyncio.gather(
            get_images(page),
            get_seller(page),
            get_details(page),
            get_features(page),
            get_shipping(page),
            get_location(page),
            get_extra_info(page)
        )

        return {
            "id": ad_id,
            "categories": categories,
            "title": title.split(" • ")[-1].strip() if " • " in title else title.strip(),
            "price": price,
            "shipping": shipping,
            "location": location,
            "views": views if views else "0",
            "description": description,
            "images": images,
            "details": details,
            "features": features,
            "seller": seller_details,
            "extra_info": extra_info,
        }
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper-Funktionen für parallelisiertes Scraping
async def get_images(page):
    try:
        return await lib.get_image_sources(page, "#viewad-image")
    except:
        return []

async def get_seller(page):
    try:
        return await lib.get_seller_details(page)
    except:
        return {}

async def get_details(page):
    try:
        return await lib.get_details(page) if await page.query_selector("#viewad-details") else {}
    except:
        return {}

async def get_features(page):
    try:
        return await lib.get_features(page) if await page.query_selector("#viewad-configuration") else {}
    except:
        return {}

async def get_shipping(page):
    try:
        shipping = await lib.get_element_content(page, ".boxedarticle--details--shipping")
        return True if shipping else False
    except:
        return False

async def get_location(page):
    try:
        return await lib.get_location(page)
    except:
        return ""

async def get_extra_info(page):
    try:
        return await lib.get_extra_info(page)
    except:
        return {}
