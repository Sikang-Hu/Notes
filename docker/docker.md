# Docker

Docker provides the ability to package and run an application in a loosely isolated environment called container. 


* Registries
* Image: a read-only template with instructions for creating a Docker container.
* Container: A runnable instance of an image.

## Command

docker rmi -f $(docker images -qa)

* docker run
  * --name="container_name"
  * -d: run in the background
  * -i: run in interactive mode
  * -t: assign a terminal for the container
  * -P: random port forwarding
  * -p: specify port forwarding:
    * ip:hostPort:containerPort
    * ip::containerPort
    * hostPort:containerPort
    * containerPort

* docker ps
  * -a:all container, including running and stopped
  * -l: last container
  * -n: last n container
  * -q
  * --no-trunc

* docker stop
* docker kill

* docker top: check the running processing
* docker inspect
* docker exec
* docker attach