# 🕸️ Wigo

![License](https://img.shields.io/github/license/neolatika/wigo)
![Status](https://img.shields.io/badge/status-active-success)
[![GitHub Release](https://img.shields.io/github/v/release/neolatika/wigo)](https://github.com/neolatika/wigo/releases)


A modern web automation framework built on Playwright with middleware, routing, cron jobs, and stealth mode.

Wigo makes browser automation simpler, modular, and powerful using an Express-like architecture combined with the reliability of Playwright.

---

## 🚀 Features

- Built on top of Playwright for reliable browser automation  
- Middleware support for before/after hooks  
- Route-based task handling  
- Cron jobs for scheduled automation  
- Stealth mode to bypass bot detection  
- Fully asynchronous design  

---

## 📦 Installation

```bash
pip install wigo
```

## 🧠 Basic Usage

```python
from wigo import WigoApp
import asyncio

app = WigoApp()

@app.before
async def before_middleware(page):
    print("Before navigation")
    await page.goto("https://example.com")

@app.after
async def after_middleware(page):
    print("After navigation")
    await page.screenshot(path="example.png")

async def main():
    await app.run("https://example.com")

asyncio.run(main())
```

## 🚀 Advanced Usage

```python
from wigo import WigoApp
from playwright.async_api import Page
import asyncio

app = WigoApp(headless=False)

# --------------------------------
# Middleware examples
# --------------------------------
@app.before
async def before_all(page: Page):
    print("Running BEFORE middleware...")

@app.after
async def after_all(page: Page):
    print("Running AFTER middleware...")

# --------------------------------
# Route (auto-opens URL)
# --------------------------------
@app.route("https://google.com")
async def google_task(page: Page):
    print("On Google page!")
    await page.wait_for_timeout(1000)

# --------------------------------
# Task (manual control)
# --------------------------------
@app.task
async def custom_task(page: Page):
    await page.goto("https://httpbin.org/get")
    print("Custom task loaded httpbin!")

# --------------------------------
# Cron job (runs every 10 seconds)
# --------------------------------
@app.cron(seconds=10)
async def repeat_task(page: Page):
    await page.goto("https://example.com")
    print("Cron job executed!")

# --------------------------------
# Run all
# --------------------------------
if __name__ == "__main__":
    asyncio.run(app.run())

```