# Spring Cloud Gateway
Spring Cloud Gateway provides a library for building an API Gateway on top of Spring WebFlux. Spring Cloud Gateway aims to provide a simple, yet effective way to route to APIs and provide cross cutting concerns to them such as: **security**, **monitoring/metrics** and **resiliency**.

* Route
* Predicate
* Filter

## Non-blocking IO
Thread-per-connection models does not suffice for high volume of request. When multiple calss to IO are done using blocking IO, for teach call a new thread is created. A thread costs around 1MB, and there are some costs due to context switching. But with non-blocking IO, we need less threads handle the same amount of IO requests. There are two kinds of blocking:

### CPU-bound blocking
In this case, the thread gets blocked because of some CPI intensive task it perform takes more time than "instantly", such as generating a bunch of prime numbers.

### IO-bound blocking
The thread gets blocked because it has to wait for data to return from an IO source.

## Spring WebFlux
