from urllib.parse import urlencode
import asyncio
from fastapi import HTTPException

from utils.browser import PlaywrightManager


async def get_inserate_klaz(browser_manager: PlaywrightManager,
                            query: str = None,
                            location: str = None,
                            radius: int = None,
                            min_price: int = None,
                            max_price: int = None,
                            page_count: int = 1):
    base_url = "https://www.ebay-kleinanzeigen.de"

    # Build the price filter part of the path
    price_path = ""
    if min_price is not None or max_price is not None:
        # Convert prices to strings; if one is None, leave its place empty
        min_price_str = str(min_price) if min_price is not None else ""
        max_price_str = str(max_price) if max_price is not None else ""
        price_path = f"/preis:{min_price_str}:{max_price_str}"

    # Build the search path with price and page information
    search_path = f"{price_path}/s-seite"
    search_path += ":{page}"

    # Build query parameters
    params = {}
    if query:
        params['keywords'] = query
    if location:
        params['locationStr'] = location
    if radius:
        params['radius'] = radius

    # Optimize: limit page_count for performance
    if page_count > 5:
        page_count = 5  # Limit to 5 pages for better performance

    # Construct the full URL and get it
    search_url = base_url + search_path + ("?" + urlencode(params) if params else "")

    page = await browser_manager.new_context_page()
    try:
        # Verbesserte Fehlerbehandlung und Timeouts
        try:
            # Optimiert: Reduzierte Wartezeit nach Navigation
            await page.goto(search_url.format(page=1), timeout=45000)
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"Navigation error: {str(e)}")
            # Zweiter Versuch mit einfacherer URL
            fallback_url = f"{base_url}/s-{query if query else ''}"
            await page.goto(fallback_url, timeout=45000)
            
        results = []

        # Nur die erste Seite scrapen, wenn Probleme auftreten
        first_page_results = await get_ads(page)
        results.extend(first_page_results)
        
        # Weitere Seiten nur laden, wenn die erste Seite erfolgreich war
        if first_page_results and page_count > 1:
            for i in range(1, page_count):
                try:
                    next_url = search_url.format(page=i+1)
                    await page.goto(next_url, timeout=45000)
                    await page.wait_for_load_state("domcontentloaded", timeout=30000)
                    
                    # Kleine Pause zwischen Seitenaufrufen
                    await asyncio.sleep(1)
                    
                    page_results = await get_ads(page)
                    if page_results:
                        results.extend(page_results)
                    else:
                        # Keine weiteren Ergebnisse - Abbrechen
                        break
                except Exception as e:
                    print(f"Failed to load page {i + 1}: {str(e)}")
                    break
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")
    finally:
        await browser_manager.close_page(page)


async def get_ads(page):
    try:
        # Kürzere Timeout für Selector-Queries
        await page.wait_for_selector(".ad-listitem", timeout=10000, state="attached")
        
        items = await page.query_selector_all(".ad-listitem:not(.is-topad):not(.badge-hint-pro-small-srp)")
        results = []
        
        # Limit Anzahl der Items für bessere Performance
        items = items[:25] if len(items) > 25 else items
        
        for item in items:
            try:
                article = await item.query_selector("article")
                if not article:
                    continue
                    
                data_adid = await article.get_attribute("data-adid")
                data_href = await article.get_attribute("data-href")
                
                if not data_adid or not data_href:
                    continue
                
                # Optimierte Selektoren für bessere Performance
                title_text = ""
                title_element = await article.query_selector("h2 a")
                if title_element:
                    title_text = await title_element.inner_text()
                
                price_text = ""
                price = await article.query_selector("p.aditem-main--middle--price-shipping--price")
                if price:
                    price_text = await price.inner_text()
                    price_text = price_text.replace("€", "").replace("VB", "").replace(".", "").strip()
                
                description_text = ""
                description = await article.query_selector("p.aditem-main--middle--description")
                if description:
                    description_text = await description.inner_text()
                
                data_href = f"https://www.kleinanzeigen.de{data_href}"
                results.append({
                    "adid": data_adid, 
                    "url": data_href, 
                    "title": title_text, 
                    "price": price_text, 
                    "description": description_text
                })
            except Exception as e:
                print(f"Error parsing ad: {str(e)}")
                continue
                
        return results
    except Exception as e:
        print(f"Error in get_ads: {str(e)}")
        return []
