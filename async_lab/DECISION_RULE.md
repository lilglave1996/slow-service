# Execution Strategy Decision Rules — WORKING RULE

## 1. Simple Work — Sequential Execution

### Choice

I would use sequential execution for simple workloads
that do not require concurrency or have operations
that depend on previous results.

### Reason

Sequential execution keeps the code simple, readable,
and easier to debug.

### Rejected Alternatives

Threads, async, and processes would introduce
unnecessary complexity and overhead when concurrency
is not needed.

## 2. Waiting-Heavy Work — Threads or Async

### Choice

I would use threads for independent blocking I/O operations and asynchronous execution when multiple independent I/O operations can overlap their waiting periods using asynchronous libraries.

### Reason

Both approaches allow independent operations to overlap their waiting periods instead of waiting for each operation to finish before starting another.

Threads are useful when working with blocking libraries, while async is useful when libraries support non-blocking operations and multiple requests need to run concurrently.

### Experimental Evidence

| Number of Requests | Sequential | Threaded | Asynchronous |
|---|---|---|---|
| 3 | 3.05 seconds | 1.02 seconds | 1.05 seconds |
| 5 | 5.08 seconds | 1.03 seconds | Not measured |

In my asynchronous HTTP experiment, I used `httpx.AsyncClient` and `asyncio.gather()` to execute three independent HTTP requests concurrently.

All three requests returned HTTP status 200. The asynchronous version completed in 1.05 seconds compared to the sequential baseline of 3.05 seconds, reducing total execution time by approximately 65.6%.

The service, endpoint, ingredients, and request count remained unchanged. The asynchronous version used a shared HTTP client.

### Asynchronous Working Rule

I would choose asynchronous execution when a workload spends most of its time waiting for independent I/O operations and the libraries support asynchronous execution. This allows waiting periods to overlap without requiring a separate thread for each operation.

Blocking calls should not execute directly inside the event-loop thread because they prevent other coroutines from progressing until the blocking operation finishes.

### Rejected Alternatives

Sequential execution was rejected for this workload because waiting times accumulate as the number of requests increases.

Processes were rejected because separate processes introduce unnecessary overhead for workloads that primarily spend their time waiting rather than computing.

Threads remain a valid alternative, especially when working with blocking libraries. My measured threaded and asynchronous results were nearly identical, so the choice should depend on library compatibility and workload requirements rather than assuming async is always faster.

## 3. CPU-Bound Work — Processes

### Choice

I would use multiple processes for independent,
CPU-intensive pure-Python workloads when parallel
execution is needed.

### Reason

Separate processes have their own Python interpreters
and GILs, allowing CPU-bound tasks to execute in
parallel across multiple CPU cores.

### Rejected Alternatives

Threads were rejected because the GIL prevents
multiple threads from executing pure-Python bytecode
simultaneously under standard CPython.

My sequential counting workload took 0.41 seconds,
while the same workload using two threads took
0.39 seconds. This small difference is consistent
with normal measurement noise.

Async was rejected because overlapping waiting periods
does not help when the workload is actively computing.

Sequential execution remains suitable for small
CPU-bound workloads, but it does not provide CPU
parallelism for larger independent workloads.

Process implementation is outside the scope of
this lesson.

## Conclusion

The execution strategy should depend on the type of workload. Simple or dependent work should remain sequential, waiting-heavy work can benefit from threads or asynchronous execution, and CPU-intensive work can benefit from processes when parallelism is needed.

My experiments demonstrated that both threads and async can significantly reduce execution time for independent I/O-bound operations, while threads provided no meaningful improvement for pure-Python CPU-bound work.

Based on the measured evidence, these decision rules have been updated from DRAFT to WORKING RULE.