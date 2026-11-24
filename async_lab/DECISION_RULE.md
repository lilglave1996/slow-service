# Execution Strategy Decision Rules — DRAFT

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

I would use threads for independent blocking I/O
operations or async when working with asynchronous
libraries and many concurrent I/O operations.

### Reason

Both approaches allow independent operations to
overlap their waiting periods instead of waiting
for each operation to finish before starting another.

In my HTTP experiment, five sequential requests took
5.08 seconds, while five threaded requests took
1.03 seconds.

### Rejected Alternatives

Sequential execution was rejected because waiting
times accumulate as the number of requests increases.

Processes were rejected because separate processes
introduce unnecessary overhead for workloads that
primarily spend their time waiting rather than computing.

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

The execution strategy should depend on the type
of workload. Simple work should remain sequential,
waiting-heavy work can benefit from threads or async,
and CPU-intensive work can benefit from processes
when parallelism is needed.