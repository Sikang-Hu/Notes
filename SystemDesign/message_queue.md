# Message Queue

Message queue is a middleware that enable the user to enqueue message and deque message from it. Its main purposes are:
* decoupling components
* asyncronization, improve responsiveness 
* Flat the peak of request

It acts as a central point of the system for message delivery, so we have requirements for it:
* High performance to avoid to become the bottleneck
* High availability
* Reliability, guarantee no message loss in edge cases
* Scalability: both scale up and scale down