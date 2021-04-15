# Database Storage I

## System Design Goals

Cost of I/O are different for different storages, volatile v.s non-volatile.

Allow the DBMS to manage database that exceed the amount of memory available.

Manage I/O carefully to avoid large stalls and performance degradation.

## Disk-Oriented DBMS

Database file are stored in pages(blocks) in disk.

In the memory, we have buffer pool, which is like a cache.

The DBMS stores a db as one or more files on disk. Early system appied custom filesystems on raw storage. But most newer DBMSs do not do this, it makes system less portable, increasing the cost of maintainance.

### Storage Manager

Responsible for maintainning a database's files. Organizes the files as a collection of pages.

A page is a fixed-size block of data. 
* Most system do not mix page types
* Some systems require a page to be self-contained.

## Arrangement 

### Slotted Pages
The most common scheme. Slot array maps "slots" to the tuples' starting position offsets. The header keeps track of the # of used slots, the offset of the starting locations of the last slot used.

### Log-Structured File Organization

DBMS stores only log records. Appends log records to the file of how the db was modified. To read, the DBMS scans the log backwards and "recreates" the tuple to find what it needs.

It is faster(image when you want to update multiple tuples in different pages), and easy to roll back. 

## Data Representation

A tuple is essentially a sequence of bytes. It's the job of the DBMS to interpret those bytes into attribute types and values. And the DBMS's catalogs contain the schema information about tables that the system uses to figure out the tuple's layout.

### Numeric

### Large Values
Most DBMSs don't allow a tuple to exceed the size of a single page. To store, DBMS uses seperate overflow pages(TOAST in postgres).

External Value Storage: store a really large value in an external file. Treated as BLOB type. However, the DBMS cannot manipulate the contents of an external file, meaning there is no durability protections or transaction protections.

More than 256kb go BLOBS, otherwise go overflows.

## System Catalogs

A DBMS stores meta-data about databases in its internal catalogs:
* Tables, columns, indexes, views
* Users, permissions
* Internal statistics
Query INFORMATION_SCHEMA t9 get info about the database.
```sql
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE table_catalog = '<db name>';
```
Shortcut in dialect: \d(postgres), SHOW TABLES(MySQL) 

* On-line Transaction Processing(OLTP): Simple queries that **read/update** a small amount of data that is related to a single entity in the db
* On-line Analytical Processing(OLAP): Complex queries that **read** lare protions of the db spanning multiple entities.
* Hyper transaction analytical processing(HTAP)

### N-ary Storage Model(NSM)
The DBMS stores all attributes for a single tuple contiguously in a page. 
**Advantages:**
* Fast inserts, updates, and deletes
* Good for queries that need tehe entire tuple.

**Disadvantages:**
* Not good for scanning large portions of the table and/or a subset of the attributes, which may bring a lot of useless data into memory.

### Decompostition Storage Model(DSM)
The DBMS stores the values of a single attribute for all tuples contiguously in a page.(Column store)

Ideal for **OLAP** workloads where read-only queries perform large scans over a subset of the table's attribtues.

To identify a tuple, there are basically two choices:
1. Fixed-length Offsets(most common): each value is the same length for an attribute.
2. Embedded tuble ids: each value is stored with its tuple id in a column.

**Advantages:**
1. Redues the amount wasted I/O because the DBMS only reads the data that it needs.
2. Better query processing and data compresssion

**Disadvantages:**
Slow for point queries, inserts, updates and deletes because of tuple splitting/stitching.

## Conclusion
1. The storage manager is not entirely independent from the rest of the DBMS. The knowledge about the storage model helps the DBMS make better choice.
2. It is important to choose the right storage model for the target workload:
   * OLTP: row store
   * OLAP: column store

## Memory Management

**Spatial Control:**
1. where to write pages on disk
2. The goal is to keep pages that are used together often as physically close together as possible on disk.

**Temporal Control:**
1. When to read pages into memory, and when to write them to disk.
2. The goal is minimize the number of stalls from having to read data from disk.

### Buffer Pool Organization 
Memory region organized as an array of **fixed-size** pages. An array entry is called a frame, which is used to store page read from the disk.

The **page table**, a in memory hash table keeping track of pages that are currently in memory. It maps page ids to frame locations in the buffer pool.

Also maintains additional meta-data **per page**:
* Dirty Flag: keep track of if the page has been modified, indicating to the storage manager that the page must be written back to the disk.
* Pin/Reference Counter: keep track of how many threads are working on the page, so that we don't evict pages in use.

### Multiple Buffer Pools

* Multiple buffer pool instances
* Per-database buffer pool
* Per-page type buffer pool

It can help reduce latch contention and improve locality.

1. Object Id: embeded an object identifier in record ids and then maintain a mapping from objects to specific buffer pools
2. Hash the page id to select which buffer pool to access.

### Pre-fetching
* Sequential Scans
* Index Scans


