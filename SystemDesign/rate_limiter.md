# Rate Limiter

Rate limiter is used to control the rate of traffic sent by a client or a service. It has following benefit:
* Prevent DOS(denial of Service) attack
* Reduce Cost. Fewer servers need to be deployed. Also control the cost for third-party APIs.
* Prevent server from overloaded. Filter out the excess requests caused by bots or misbehavior.

We have following requirement for it:
* Low latency: rate limiter should not slow down HHTP response time
* Use as little resource as possible
* Distributed, shared across multiple servers or process
* Exception handling, say a user reaches its limit.
* High availablity

Cloud microservices have become widely popular and rate limiting is usually implemented in API gateway. But whethere 