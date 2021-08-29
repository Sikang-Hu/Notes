# MySQL note

## Index 

Drawback of Hash Index:
* Cannot sort
* Not support leftmost matching principle
* If there are many duplicated keys, the hash collision will ruin the performace
* Not support range query

Clustering V.S. Secondary
* Clustering Index stores the data at the leaf, while secondary stores the primary key and the indexed column.
* Clustering is created by primary key, while secondary index is created by non-primary key. 
* Every secondary index will result to a index tree, which costs space.
* If the column in a query is included in the secondary index key, then it doesn't need to go back to the table.

**Leftmost matching principle:**

The index can be used to find a key. But when it comes to range query(`>, <, between, like(left match, abc%)`), the next key will be unordered, which can only be queried by scanning index tree.

Note: 
* Index column should not be put in calculation, otherwise all row will be scanned to calculate the value for comparing. `f(idx) = y` should be write as (`idx = f'(y)`);
* Better to extend current index, instead of creating a new index.
* Choose the more distinguished column as the index.


## Lock

* Read-read conflict
* Read-write conflict
* Write-write conflict

### Table lock & row lock
Table lock:
* Lower cost
* No dead lock
* Apt to have conflict
* Lower concurrency

Row lock:(in InnoDB)
* Higher cost, slow to acquire
* Dead lock
* Lower probability to have conflict
* Higher concurrency

Row lock only applies when there is query for index. Also, index speeds up the query but slows down insertion/updating/deleting.

In mysql, write lock has higher priority than read look.

### Row lock
* S Lock: also read lock, shared the resource with other read, but prevent X lock
* X lock: mutual exclusive to all the other lock, blocking other locks.

### Intention lock

Indicate current modification to a table, so that we can have both table lock and row lock.

* IS: transaction intents to added a S lock to a row in this table, must be acquired before adding S lock
* IX: transaction intents to added a X lock to a row in this table, must be acquired before adding X lock

### Gap lock
When doing range query, not equality query, and request for a lock, InnoDB will add lock for the index in the range. For those indices with no record, the lock is called gap lock. Gap lock only applies in RR. Gap lock prevents the phantom read.

### Dead lock
Rollback of mysql can solve a lot of dead locks, but it is unavoidable. Following rule-of-thumb can help us avoid dead lock:
* Query the table or rows in the same order, to prevents different transactions hold parts of the resource.
* Decomposite big transaction so that less resource will be held/
* If bussiness requirement allowed, downgrade the isoaltion level also helps. e.g. from RR to RC to avoid gap lock
* Lock all the needed resource at one time in a transaction
* Add proper index so that less row lock will apply. (Otherwise, each row will be locked)

## Transaction isolation level

## Read uncommitted

## Read committed

When write, lock the row with X lock if a condition is indexed, otherwise the Innodb will first lock the whole table, and let the server to filter unrelated row and release the lock. When read, no lock is needed.

## Optimistic VS Pessimistic

Optimistic lock is when you check if the record was updated by someone else before you commit the transaction. Pessimistic locking is when you take an exclusive lock so that no one else can start modifying the record.

## Repeatable Read (Defaulti in mysql)

## Serializable

## MVCC in MySQL

### row trx_id

In read committed, every time there is a statement, there will be a new snapshot generated. In repeatable read, a global snapshot for this transaction will be generated at the beginning of the transaction.

### Current Read

### Snapshot Read