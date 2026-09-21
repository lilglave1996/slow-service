# slow-service

A tiny Flask API that is **slow on purpose**. Every nutrition lookup takes about
one second. It stands in for any real dependency that makes your code wait — a
payment provider, a third-party API, a database on another machine.

BE105 Unit 3 uses it to make asynchronous programming visible: call it five
times in a `for` loop and you wait five seconds; call it five times concurrently
with `asyncio` and `httpx` and you wait one. Unit 4 turns it into the first
"other service" your gateway talks to.

## Run it

```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                   # serves on http://127.0.0.1:5001
```

Runs on port **5001** so it can sit next to the recipe API on 5000.

## Endpoints

| Method | Path | Behaviour |
|---|---|---|
| GET | / | describes the service |
| GET | /health | answers immediately (`{"status": "ok"}`) |
| GET | /nutrition/&lt;ingredient&gt; | waits ~1 s, then returns fake per-100 g nutrition for the ingredient (stable numbers for a given name; unknown ingredients still succeed) |

Example:

```
time curl -s http://127.0.0.1:5001/nutrition/eggs
# {"calories":155,"carbs_g":1.1,"fat_g":11.0,"ingredient":"eggs","per":"100 g","protein_g":13.0,"took_seconds":1.0}
# real 0m1.02s
```

## Measure the wait yourself

Sequential — five lookups, about five seconds:

```python
import time, httpx

ingredients = ["eggs", "tomatoes", "peppers", "onion", "cumin"]
start = time.perf_counter()
for name in ingredients:
    httpx.get(f"http://127.0.0.1:5001/nutrition/{name}")
print(f"{time.perf_counter() - start:.1f} s")   # ~5.0 s
```

Concurrent — the same five lookups, about one second:

```python
import asyncio, time, httpx

async def main():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        await asyncio.gather(*(client.get(f"http://127.0.0.1:5001/nutrition/{n}") for n in ingredients))
        print(f"{time.perf_counter() - start:.1f} s")   # ~1.0 s

asyncio.run(main())
```

The numbers are fake. The waiting is real.
