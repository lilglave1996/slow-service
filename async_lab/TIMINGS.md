
# Synchronous HTTP Timing Baseline

## Sequential Requests

| Number of Calls | Total Time |
|---|---|
| 1 | 1.05 seconds |
| 3 | 3.05 seconds |
| 5 | 5.08 seconds |

## Observations

Each synchronous HTTP request must finish before the next begins.

As the number of sequential requests increases, the total execution time increases approximately linearly.

These measurements establish a baseline for comparing synchronous and asynchronous execution.

