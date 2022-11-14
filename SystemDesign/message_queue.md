# Message Queue

Message queue is a middleware that enable the user to enqueue message and deque message from it. Its main purposes are:
* decoupling components
* asyncronization, improve responsiveness 
* Flatten the peak of request

It acts as a central point of the system for message delivery, so we have requirements for it:
* High performance to avoid to become the bottleneck
* High availability
* Reliability, guarantee no message loss in edge cases
* Scalability: both scale up and scale down

## High availability
* For Kafka, the message will be replicated to follower, and once the configured number of node receives the message, it can be 0, 1, all, depending on the application's requirement
* For rabbitmq, there are two mode publisher confirms or transaction
  * transaction: the message will be accepted by all brokers and then the client will commit or rollback. This is synchronized. blocking.
  * publisher confirms: the client pass a non-ack callback, if a node is not reachable, the message will not be ack and callback is triggered, this is async. 
  * For mirror queue, all replications in the cluster need to accept the message, while in quorum queue, only majority is enough.
