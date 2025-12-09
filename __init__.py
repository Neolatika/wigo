"""
Wigo - A web automation framework built on Playwright with middleware support.
"""

from .__version__ import __version__

import asyncio
import traceback
from functools import wraps
from typing import Callable, Awaitable, Optional
from playwright.async_api import async_playwright, Page
from playwright_stealth import Stealth

__all__ = ['WigoApp', '__version__']


class WigoApp:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.before_middlewares = []
        self.after_middlewares = []
        self.tasks = []
    
    # --------------------------------
    # Middleware
    # --------------------------------
    def before(self, func):
        self.before_middlewares.append(func)
        return func

    def after(self, func):
        self.after_middlewares.append(func)
        return func
    
    # --------------------------------
    # Core executor
    # --------------------------------
    def _build_wrapper(self, func: Callable[..., Awaitable], url: Optional[str] = None, retries: int = 0):
        @wraps(func)
        async def wrapper():
            for attempt in range(retries + 1):
                try:
                    async with Stealth().use_async(async_playwright()) as pw:
                        browser = await pw.chromium.launch(headless=self.headless)
                        context = await browser.new_context(viewport={"width": 1400, "height": 900})

                        page = await context.new_page()

                        # Middleware: before
                        for m in self.before_middlewares:
                            await m(page)

                        # Auto open URL
                        if url:
                            await page.goto(url)

                        # Main task
                        await func(page)

                        # Middleware: after
                        for m in self.after_middlewares:
                            await m(page)

                        await context.close()
                        await browser.close()
                        return  # success

                except Exception as e:
                    print(f"[ERROR - Attempt {attempt+1}] {e}")
                    traceback.print_exc()
                    if attempt == retries:
                        print("Max retries reached, aborting.")
            
        return wrapper

    # --------------------------------
    # Decorators
    # --------------------------------
    def task(self, func):
        wrapper = self._build_wrapper(func)
        self.tasks.append(wrapper)
        return wrapper
    
    def route(self, url: str):
        def decorator(func):
            wrapper = self._build_wrapper(func, url=url)
            self.tasks.append(wrapper)
            return wrapper
        return decorator

    def cron(self, seconds: int):
        def decorator(func):
            wrapper = self._build_wrapper(func)
            async def loop_runner():
                while True:
                    await wrapper()
                    await asyncio.sleep(seconds)
            self.tasks.append(loop_runner)
            return wrapper
        return decorator

    # --------------------------------
    # Run all tasks
    # --------------------------------
    async def run(self):
        await asyncio.gather(*(asyncio.create_task(task()) for task in self.tasks))


# # =============================================
# # 🚀 Usage Example
# # =============================================
# app = WigoApp(headless=False)


# # --------------------------------
# # Middleware examples
# # --------------------------------
# @app.before
# async def before_all(page: Page):
#     print("Running BEFORE middleware...")


# @app.after
# async def after_all(page: Page):
#     print("Running AFTER middleware...")


# # --------------------------------
# # Route (auto-opens URL)
# # --------------------------------
# @app.route("https://google.com")
# async def google_task(page: Page):
#     print("On Google page!")
#     await page.wait_for_timeout(1000)


# # --------------------------------
# # Task (manual control)
# # --------------------------------
# @app.task
# async def custom_task(page: Page):
#     await page.goto("https://httpbin.org/get")
#     print("Custom task loaded httpbin!")


# # --------------------------------
# # Cron job (runs every 10 seconds)
# # --------------------------------
# @app.cron(seconds=10)
# async def repeat_task(page: Page):
#     await page.goto("https://example.com")
#     print("Cron job executed!")


# # --------------------------------
# # Run all
# # --------------------------------
# if __name__ == "__main__":
#     asyncio.run(app.run())
