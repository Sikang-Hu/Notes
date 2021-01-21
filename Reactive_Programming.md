# Reactive Programming

Reactive programming is about **non-blocking** applications that are **asynchronous** and **event-driven** and
require a small number of threads to scale vertically ranther than horizontally. 

Reactive types are not intended to allow you to process the request or data faster. They introduce a small overhead compared to regular blocking processing to strength their capacity to serve more request concurrently, and to handle operations with latency.

Vertically: within the JVM
Horizontally: through clustering

Backpressure: a mechanism to ensure producers don't overwhelm consumers.

## Advantages

1. High-performance
2. Concurrency
3. Asynchronous operations
4. Non-blocking IO

## Use Cases

* External Service Calls: backend services based on REST-ful API are fundamentally blocking and synchronous.
* Highly Cnncurrent Message Consumers
* Abstract Over Asynchronous Processing

