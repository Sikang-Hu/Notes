# Spark Note

## RDD, DataFrame and DataSet

### RDD
Resilient Distributed Dataset, it is Read-only partition collection of records, which allows a programmer to perform in-memory computations on large clusters in a fault-tolerant manner.

### DataFrame
In DataFrame, data organized into named columns. It is an structured immutable distributed collection of data, allowing higher-level abstraction.

### DataSets
An extension of DataFrame, which provided type-safe, object-oriented programming interface. It takes advantage of Spark's Catalyst optimizer by exposing expressions and data fields to a query planner.

## RDD Operations
RDD supports two types of operations: transformations, which create a new dataset from an existing one, and actions, which return a value to drive program after running a computations on the dataset.

All transformations in Spark are **lazy**, they do not compute the results right away, but just remember the transformations applied to some based dataset. The transformations are only computed when an action requires a result to be returned to the driver program.

By default, each transformed RDD may be recomputed each time an action run on it. However, you may persist an RDD in memory using persist(or cache) method.