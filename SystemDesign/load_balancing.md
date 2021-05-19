# Load Balancine

## Benefit
* Faster and uninterrupted service.
* High availability and throughput
* Predictive analytics that determine traffic bottlenecks before they happen.
* System administrators experience fewer failed or stressed components. Instead of a single device performing a lot of work, load balancing has several devices perform a little bit of work.
* Load balancing makes it easier for system administrators to handle incoming requests while decreasing wait time for users.

## Algorithm

Load balancers consider two factors before forwarding a request.
1. Appropriate server for the request.
2. Pick a healthy server

### Health Checks
The load balancer regularly attempt to connect to backend servers to ensure they are listening. If a server fails, it will be removed from the pool and no throughput will be forwarded to it until it responds to health check again.

### Algorithms
1. **Least Connection Method** - directs traffic to the server with fewest active connections. This approach applies when there are a large number of persistent client connections which are unevenly distributed between server.
2. **Least Response Time Method** - pick server with fewest active connections and lowest average response time.
3. **Least Bandwidth Method** - Select server currently serving the least amount of traffic measured in megabit per second.
4. **Round Robin Method** - Cycles through a list of servers and sends each new request to the next server. It applies when the server are of equal specification and there are not many persistent connections.
5. **Weighted Round Robin Method** - Assign weight to each server according to the processing capabilities. Server with higher weights receive new connections before those with less processing capacity.
6. **IP Hash** - Calculate the hash of OP address of a client to redirect.

## Redundant Load Balancers

The load balancer can be a single point of failure; to overcome, we can construct a cluster with two LB, each of them monitors the other. 

## Reference
* [What is load balancing](https://avinetworks.com/what-is-load-balancing/)
* [Introduction to Architecting Systems](https://lethain.com/introduction-to-architecting-systems-for-scale/)