# Lecture 02 MapReduce and Spark

## Review
> Who is responsible to not "lose" objects?
MapReduce/Spark: when the deserializer does not find the end of the chunk, it just ask for the next chunk. Mapper will look for the beginning of a new object, if it does not find, there is no input for that mapper (this is a segment of previous chunk).

Intermediate key is the most important, since it determines how the map/reduce will work, controlling the grouping, and we cannot intervene how to interpret then during the process.

## Map task v.s. Map call
Number of tasks depends on the numebr of input split, while the number of map calls depends on how many objects input to the function, for example, in word count, a single line is an object.

## Reduce task v.s. Reduce call
By default, the number of reduce task is f(cluster & input size), the number of reduce calls is the number of distinct keys in mapper output.

Why implement its own datatype: makes those datatype more adjustable for serialization or deserialization.

## Lazy execution in Spark
Spark knows that sum() is next, hence can already combine during the grouping.(Like the query optimizater in SQL)

```
D2 = D1.groupBy("word")
D2.sum("count")
```

After grouping, the type of the DataSet changes.
```
D1 - DataSet
D2 = D1.groupBy(...) //RelationalGroupedDataSet
```
XYZ.sum() behvaes differently depending on XYZ being a DataSet or RelationalGroupedDS.

Does this apply combining? Yes, same as D1.groupBy.Sum
Does it compute a sum per group of sum of global? Sum per group.

## Transformation v.s. Action
Transformation: defines step for a computation, does not trigger execution, like D1.groupBy(...)
Action: Applies some "final" aggregation or writes the RDD "out", triggers immediate execution.

## Sorting

1. Range Partitioner(TotalOrderPartitioner) defined by a sequence of "increasing values"
2. Data in each Reduce task is sorted by key automatically.


Sort in user code is a bad idea, since there could be some caveats such as the chunk size does not fit the memory size.

If no reducer is needed, just set the #reducer to 0 instead of using a identity reducer

## Reduce-side join vs. Replicated join:
* |S| vs. |T|
* # machines
* note: if the output is huge, difference between input size is negligible regarding the output size.
* In the case of Self-join, replicated join will be problematic, since both data set will be huge.

## For hw2
Using "Max-filter" to remove edges and estimate the # triangles.

## For hw3
remove broadcast what happens.