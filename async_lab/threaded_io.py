import httpx
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:5001"

ingredients = ["eggs", "tomatoes", "peppers", "onion", "cumin"]


def fetch_nutrition(ingredient):
    response = httpx.get(f"{BASE_URL}/nutrition/{ingredient}")
    response.raise_for_status()
    return ingredient, response.json()


for count in [1, 3, 5]:
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = dict(
            executor.map(fetch_nutrition, ingredients[:count])
        )

    elapsed_time = time.perf_counter() - start_time

    print(f"{count} calls: {elapsed_time:.2f} seconds")
    