# ElasticSearch

## Scalability and Resilience

Servers(nodes) can be added to a cluster to increase capacity and Elasticsearch automatically distributes your data and query load across all of the available nodes.

Index is a logical grouping of one or more physical shards, where each shard is actually a self contained index. By distributing the documents in an index across multiple  shards, and distributing those shards across multiple nodes, Elasticsearch can ensure redundancy. Shards can be either primary shards and replicas. The number of primary shards in an index is fixed at the time that an index is created, while the number of replicas can vary any time. 

## Performance Considerations

The more the shards, the more overhead there is in maintaining those indices, though the query speed can be faster. The size of shards will affect the time needed for migration, the ability of ES to rebalance. 

Here are some rule-of-thumbs:

* Aim to keep the average size between a few GB and a few tens of GB, usually 20-40 for time-based data.

* Avoid too many shards. The number of shards a node can hold is proportional to the available heap space, usually less than 20 per GB.

[Test Configuration with Data](https://www.elastic.co/elasticon/conf/2016/sf/quantitative-cluster-sizing) 

Cross-cluster replication(CCR) is a secendary remote cluster that can serve as a hot backup. It automatically sybchronized indices from the primary cluster and can take over if there is a major outage. CCR is read-only.

/_cat/heath?v to check the status of cluster

Using [bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/7.5/docs-bulk.html) to batch document operations is extremely faster than sending request separately.

## Mapping from Document to Shard

Elasticsearch applies a hash function on _routing to decide which shards a document goes:

```python
shard = hash(_routing) % number_of_primary_shards
```

## Data Replication Model

Each index is divided into shards and each can have multiple copies. These copies form a replication group and must be sync when documents are added or removed. 

This model is based on primary-backup model, where a single copy from the replication group acts as the primary shard, while the other are replica shards. The primary shards are the entry point for all indexing operations and is responsible to replicate varified operation to other copies.

If a replica misses a operation, the node hosting the primary shard will report to master node to request removing that replcia from the group. Once the removal has been acknowledged by the master node, the primary acknowledge the operation. The master will also instruct another node to build a new shard copy for that.

If a priamry shards has been isolated due to a network partition, it may be demote by the master node. However, it might not realize that and continue to deal with incoming indexing operations and relicate them to replcia. Operation cam from a stale primary will be rejected by the replicas. When the primary receives a response from the replica rejecting its request because it is no longer the primary then it will reach out to the master and will learn that it has been replaced.

### Read Model

When a read request is received by a node, that node is responsible for forwarding it to the nodes that hold the relevant shards, collating the respoonses and responding to the client. This node is a **coordinating node** for that request.

1. Resolve the requests to relevant shards
2. Select an active copy of each relevant shard. By default, it will just round robin between the shard copies
3. Send the requests to the selected copies
4. Combine the results and respond.

### Shard failure

If the shards fail to respond to a read request, the coordinating nodes sends the request to another shard copy in the same replication group. Some API will return partial response with 200 OK, while the failure is indicated through timed_out and _shards.

### Simple Implications

* Normally, each read operation is performed once for each relevant replicaiton group.

* The primary first indexes locally and then replicates the request, so a concurrent read could see a unacknowledged change.

* Two copies by default.

### Failure

* The primary waits for all replicas in the in-sync copies set during each operation, so a single slow shard can slow down the entire group. A single slow node also slows down the search for the similar reason.

* The primary can expose unacknowledged writes, since it will only realize to be isolated after sending requests to its replicas or reaching out to the master. At that time, the operation is already indexed into the primary and can be read by a concurrent read. Elasticsearch mitigates this by letting the primary ping the master node every second and rejecting indexing operations if no master is known.

## Refresh

Shards are minimal units in ES, which is built on the index in Lucene. In Lucene, an index contains a lot of segments, which is self-contained and immutable.

Every time a document is inserted, there will be a new segment. A new document will be written into the **Index Buffer**, and Refresh will then write data in the buffer into a segment, then the data can be access. The frequency of Refresh is every second by default, and can be configured with index.refresh_interval. Full buffer will also trigger Refresh.(10% of JVM by default).

## Transaction Log

The newly inserted document will first be stored in memory to avoid costy I/O to the disk. While at the same time, the data will also be written into transaction log and then will be write in to hard drive by default.

## ES Flush

First Refresh to empty the index buffer. Then call fsync to write segments in cache to the disk. It will be executed every 30 minutes by default, or the transaction log is full(512MB by default).

## ES Merge

Merge segments to reduce the number of segments, and delete the file marked as deleted. 

Merge will temporary increase the storage of a shard as documents of the segments need to be put into a new one.

[Introduction to Merge](http://blog.mikemccandless.com/2011/02/visualizing-lucenes-segment-merges.html)

## Search Procedure

### Query

When receicing a request from the user, a node will act as a coorddinating node to forward the query request to shards. Selected shards will then query in themselves and sort the result, and then response with *From+Size* Ids and ranks to the coordinating node.

### Fetch

Collect all the id and ranks from all the shards and sort again. Then select *from+size* id, fetch the data from shards by multi-get.

### Performance

Each Node need to get from + size documents, and the coordinate node need to deal with shards * (from + size) docs. So, more shards will consume more resource. Also, the relevant value will also deviate, since each shards compute it with its own data.

## Pagination

## Optimistic Concurrency Control

To ensure an old version never overwrite a new version, every operation performed to a document is assigned a sequence number by the primary shard that coordinates that change.

The _seq_no and _primary_term uniquely identify a change. By noting down the sequence number and primary term returned, we can make sure to only change the document if no other change was made to it since retrieved.

## Frozen Indices

For data which are rarely accessed(such as old logs in time series data set.), freezing it will release the memory it occupied, and only transient data structure will be built for query such indices. However, future query will become costy since it takes time to rebuild the data structure in the memory.

## Tuning for Indexing Speed

### Use Bulk Request

Using bulk request will yield much better performance than single-document index requests. To know the optimal size of a bulk request, we can run a **benchmark test** on a single node with a single shardm with size begining from 100 and doubling every time. Large bulk request will overwhelm the server's memory, so just keep it within **tens of megabytes** per request.

### Sending Data from Multiple Workers/threads

### Unset or Increase the Refresh Interval

### Auto Generated ID

### Indexing Buffer Size

At most 512 MB indexing buffer per shard with indices.memory.index_buffer_size.

## Tuning for Search Speed

### Give memory to File system cache

At least half of the available memory.

### Mapping Identifier as *keyword*

### Search Rounded Dates

Queried time stamp will be cached for later use, future hit will be faster.

## Scroll API

### Transiant

In ElasticSearch, scrolling does not keep track of the lastet status of index. Instead, it is just a **snapshot** of the index at the time the scrolling request initialed. It will **ignore any subsequent changes** to these documents.

Hence, scrolling is intended for processing large scale of data, instead of for real time user requests.

The *scroll_id* indentifies a search context, i.e. the snapshot. The context is create by the initial context and kept alive by subsequent requests.

Even though some document will be deleted(updated) during the scrolling, the deleted documents still exist in the segements. Merge will also happen during that time. While open search context will prevent the old segments from being deleted since they are still in use. However, this will bring issues if too many scrollings opened.

## Script API

Script API brings the possibility to evaluate custom expression in Elasticsearch. The default scripting language is Painless. 

## Update API

Update a document using the specified script.
