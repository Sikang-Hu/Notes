# Advanced SQL

* While relational database is based on set algebra, SQL is based on bags algebra, i.e. unordered, allow duplicates.

* Aggregate functions: a function that you define in the **output** list of your select statement that is gonna take as input multiple tuples and perform some kind of aggregation on top of that and produced a single result.

* Non-aggregated values in SELECT out clause must appear in GROUP BY clause. However, in traditional sql_mode of mysql, it is tolerable, but in `ansi` mode, it is not allowed.

* In some sql system, queries can be optimized the claused shows up later in the query plan, e.g. the clause in HAVING can be used to filter out the unnecesarry work.

* Common Table Expressions