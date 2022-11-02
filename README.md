# Container Demo #

This is a quick demo to show what containers are and how to use them. The examples in this demonstration use Docker. 

## Container Basics ##

A container allows us to run a process in an isolated environment. Similar to a VM but much lighter weight. Unlike VM's containers share the same running kernel as the host.

### Image vs. Container ###
Images are compressed, read-only filesystems


### Persisting Data ###
#### Volumes ####
#### Bind Mounts ####

### Some Handy Commands ###
#### Stop all docker containers ####
```
docker stop `docker ps --all | awk '{print $1}' | grep -v CONTAINER`
```
#### Stop all docker containers ####
```
docker rm `docker ps --all | awk '{print $1}' | grep -v CONTAINER`
```

#### Remove all docker images. ####
```
docker image rm `docker image ls --all | awk '{print $3}' | grep -v IMAGE`
```