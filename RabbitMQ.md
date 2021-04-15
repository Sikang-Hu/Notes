# RabbitMQ

## Populur MQ
* ActiveMQ: developed by Apache
* Kafka: developed by LinkedIn, originally in scala. It was designed to cope with high thoughput, while lost the consistency, integrity and support for the transaction. Used in big data, for responsiveness.
* RocketMQ: Developed by Alibaba in Java, derived from the Kafka but enhanced the reliability and trasactional management.
* RabbitMQ: Developed using Erlang, based on AMQP protocol. More reliable than Kafka, but less throughput. Consistence and fault-tolerant.

## AMQP 
Advanced message queuing protocol.

## Provider & Consumer

server, virtual host, exchange, queue

## Work queues(Task queues)

## Use Cases

* Asyncronize to improve responsiveness
* Decoupling
* Decreasing the peak: maximum request, discard the message immediately if exceeded the maximum.