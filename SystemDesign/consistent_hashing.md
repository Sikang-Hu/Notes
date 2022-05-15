# Consistent Hashing

Distributed Hash Table is one of the fundamental components used in distributed scalable systems. Given n cache server, An intuitive hash function woould be key % n. But it has two major drawbacks:
* not horizontally scalable. If a new cache host is added, all existing mappings are broken. Also, it becomes difficult to schedule a downtime to update all caching mappings.
* not load balanced. The data is not distibuted uniformly in most cases. For the caching system, it translates into some cahces becoming hot and saturated while the others idle and are almost empty.

## What is Consistent Hashing

Consistent hashing is a special kind of hashing which uses a hash function which changes minimally as the range of hash function changes. It operates independently of the number of servers or objects in a distributed hash table by assigning them a position on a abstract circle, or hash ring.

## How does it work

The key is hashed and assigned to the next server on the ring.

If a new server added, only some keys from its next server will be reassigned to it. only (1/n) fraction of objects.

When a server is removed, its key will be added to the server next to it on the ring.

To implement the *lookup and insert*, we need the successor operation. The binary search tree is a good option.

### Reducing the variance

While the xpected load of each cache server is a 1/n fraction of the objects, the realized load of each cache will vary. An easy way to decrease this variance is to make k "virtual copies" of each caches s, implemented by hashing its name with k different hash functions, and assign them on the ring. If we have 3 servers and 4 copies per server, we will choose 12 points on the circle. The objects are still assigned as before by scanning rightward. 

This increase the number of keys stored in the balanced binary search tree by a factor of k, but reduces the variance inload across cache servers significantly. Though some copies will get more objects than expected, but this will be largely canceled out by other copies taht get fewer than expected.

Choose k around logN (n is number of servers) is large enough to obtain reasonably balanced loads.