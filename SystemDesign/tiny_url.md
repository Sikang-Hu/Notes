# Tiny Url

## Offline Key Generation Service


## Data partition

* Range Based Partitioning
* Hash-Based Partitioning

## Cache

## Load Balancer

round robin

## Purge and DB cleanup

* Lazy cleanup, when user tries to access an expired link, we can delete the link and return an error
* A separate Cleanup service can run periodically. It should be lightweight and scheduled to run only when the user traffic is expected to be low.
* default expiration time for each link
* after deletion, we put the key back to key-DB for reuse
* 