# Heartbeat Service

Usually, multiple servers form a cluster to provide service. In case there is a node falls down, the cluster should be aware of that to ensure fault tolerance. Then, we need the heartbeat service. Each server need to report their heartbeat to a management server so that the manager can discover the new machine and timed-out machine.

## Timed-out Determine Algorithm

The naive solution is to iterate through all the machine to find the timed-out machine(say `cur ts - last ts >= 5s`), but it is not scalable as the time complexity is O(n). 

We can use the LRU to maintain the lastest occurrence of nodes. Every time we receive a new heart beat message, we add it to the LRU, which is O(1). And we can always look at the beginning of the list for the earlist received heartbeat to see if the corresponding machine is offline.

## High Throughput

First, we will adopt multi-threads to full utilize the multi-core CPU.
* `epoll` to listing to multiple sockets
* load balancing via ip address. The dispatching thread will dispatch heartbeat package to worker threads based on the hash of the ip. In this way, the workers are isolated.
* 1 buffer queue per thread. Since 1 queue is accessed by both dispatcher and worker, so the lock is required. It is better to use a spinning lock to avoid context switch.
* If thread is executed on different core, the L1, L2 cache will hardly be hit. So, we can use `sched_setaffinity` to bind a thread to a core.
* Default mem allocator on Linux is `PtMalloc2`, it is not efficient when allocate small piece of memory under multithread. Google's `TCMalloc` is good at it.

## Transport Layer

* If the length of the heartbeat package is less than MTU, we can choose UDP, as UDP is simpler, and package loss for heartbeat service is tolerable.
* If it is larger than MTU, we need TCP. If sending datafram longer than 1500 bytes, IP protocol will split the datagram, and reassemble it at receiving. But it is not efficient as TCP.
* If we chose TCP, we need to set the `ulimit` to increase the number of file descriptors a process can have. `/proc/sys/fs/file-nr`
* Also, we need to optimize the hand-shaking, buffer and congestion control algorithm. Google's BBR algo is bandwidth and delay based, which is more sensitive to the congestion.