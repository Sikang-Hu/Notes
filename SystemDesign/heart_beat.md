# Heartbeat Service

Usually, multiple servers form a cluster to provide service. In case there is a node falls down, the cluster should be aware of that to ensure fault tolerance. Then, we need the heartbeat service. Each server need to report their heartbeat to a management server so that the manager can discover the new machine and timed-out machine.

## Timed-out Determine Algorithm

The naive solution is to iterate through all the machine to find the timed-out machine. 

## High Throughput

## Transport Layer