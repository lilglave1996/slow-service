
import httpx
import time

BASE_URL = "http://127.0.0.1:5001"

ingredients = ["eggs", "tomatoes", "peppers", "onion", "cumin"]

for count in [1, 3, 5]:
    start_time = time.perf_counter()

    for ingredient in ingredients[:count]:
        response = httpx.get(f"{BASE_URL}/nutrition/{ingredient}")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"{count} calls: {elapsed_time:.2f} seconds")
