# HTTP Timing Comparison

## Sequential and Threaded Requests

| Number of Calls | Sequential Time | Threaded Time |
|---|---|---|
| 1 | 1.05 seconds | 1.05 seconds |
| 3 | 3.05 seconds | 1.02 seconds |
| 5 | 5.08 seconds | 1.03 seconds |

## Sequential Observations

Each synchronous HTTP request must finish before the next begins.

As the number of sequential requests increases, the total execution time increases approximately linearly.

These measurements establish a baseline for comparing synchronous and asynchronous execution.

## Threaded Observations

Using ThreadPoolExecutor allows independent HTTP requests to execute concurrently and overlap their waiting periods.

The threaded execution time remains close to one second regardless of whether one, three, or five requests are made.

The five-call workload decreased from 5.08 seconds to 1.03 seconds, reducing the total execution time by approximately 79.7%.

The threads overlap waiting periods rather than making the slow service itself faster.

## Fairness Note

Both execution strategies used the same slow-service endpoint, ingredients, request counts, and local environment.

The original sequential baseline measurements remain unchanged. The main difference between the two experiments is the execution strategy.

## CPU-Bound Workload Comparison

| Execution Strategy | Total Time |
|---|---|
| Sequential | 0.41 seconds |
| Two Threads | 0.39 seconds |

### Observations

Both execution strategies performed the same total
workload of 20 million counting operations.

The threaded version was only 0.02 seconds faster
than the sequential version. This small difference
is consistent with normal measurement noise.

The results matched my prediction because the Global
Interpreter Lock (GIL) prevents multiple threads
from executing pure-Python bytecode simultaneously
under standard CPython.

Unlike I/O-bound workloads, CPU-bound workloads do
not benefit significantly from threading in this
experiment.