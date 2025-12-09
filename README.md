# Wigo

A web automation framework built on Playwright with middleware support for browser automation tasks.

## Features

- Built on top of Playwright for reliable browser automation
- Middleware support for before/after hooks
- Stealth mode to avoid bot detection
- Asynchronous by design

## Installation

```bash
pip install wigo
```

## Usage

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

## License

MIT
