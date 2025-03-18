from playwright.async_api import async_playwright

def get_random_ua():
    # Einen festen modernen User-Agent zurückgeben, da random hier nicht nötig ist
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

class PlaywrightManager:
    def __init__(self):
        self._playwright = None
        self._browser = None
        
    async def start(self):
        from playwright.async_api import async_playwright
        self._playwright = await async_playwright().start()
        # Browser-Launch optimieren mit reduzierten Ressourcen
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-gpu',                
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-sandbox',
                '--single-process',
                '--disable-extensions',
            ]
        )
        
    async def new_context_page(self):
        if not self._browser:
            await self.start()
            
        # Optimierte Kontext-Einstellungen
        context = await self._browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent=get_random_ua(),
            java_script_enabled=True,
            is_mobile=False,
            locale='de-DE',
        )
        
        page = await context.new_page()
        # Längere Timeouts für instabile Verbindungen
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        return page
        
    async def close_page(self, page):
        if page:
            try:
                await page.close()
            except:
                pass
         
    async def close(self):
        if self._browser:
            try:
                await self._browser.close()
            except:
                pass
        if self._playwright:
            try:
                await self._playwright.stop()
            except:
                pass
            