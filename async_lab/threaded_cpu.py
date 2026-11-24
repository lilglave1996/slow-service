import time
from concurrent.futures import ThreadPoolExecutor

COUNT = 10_000_000


def count_work(n):
    total = 0
    for _ in range(n):
        total += 1
    return total


# Sequential execution
start_time = time.perf_counter()

result1 = count_work(COUNT)
result2 = count_work(COUNT)

elapsed_time = time.perf_counter() - start_time

print(f"Sequential: {elapsed_time:.2f} seconds")


# Threaded execution
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=2) as executor:
    future1 = executor.submit(count_work, COUNT)
    future2 = executor.submit(count_work, COUNT)

    result1 = future1.result()
    result2 = future2.result()

elapsed_time = time.perf_counter() - start_time

print(f"Two threads: {elapsed_time:.2f} seconds")
