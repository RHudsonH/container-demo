# Container Demo #

These are the demonstration files that accompany an Intruduciton to Containers. Which is a webinar presented as a part of the Mark III Education series.

The webinar begins with a brief set of slides found in `Container Basics.pptx` and then transitions to a live demo.

During the live demo, we walk through a series of very similar containers that serve to show the basics of containerizing a workflow, accessing data from withing a running containers and saving files out of the containers. We start with the `black-and-white` directory.

## Black and white.

This being the first container, we will thorougly explore the directories contents.

### 1. `blackandwhite.py`
This file contains a simple python script that will open the file specified int the environment variable `IN_FILE`, convert the image to black and white and then save the file out to the location specified in another environment variable named `OUT_FILE`.

This script uses environment variables to set the required parameters. However, we could have use command line parameters which could be passed to docker when we create the container.   

### 2.  `requirements.txt`
This file lists the library requirements for the script `blackandwhite.py`. There's only one line here as there is only one required non-standard python library. 

### 3. `Dockerfile`
The file that will instruct `docker` on how to build the image we want to run our script. 

In looking through this file it is helpful to point out a number of things that are helpful to understand as the demo progresses.
 
1. On the line that begins with 'FROM' we are specifing the base container that we will be building on. This base image was chosen as it provides a jummping off point that is close to what we want our final image to look like. We could start with some other base image. For example if we wanted to start with an image that didn't already have python installed, we could do so, but then we would have to make sure to include all of the necessary commands to install python. This could allow us to do a custom build of python.

1. Also on the line beginning with 'FROM' we encounter the image naming syntax `CONTAINER NAME`:`TAG`. In this case it's `python:3.10.4`. This means we will start with a python base container which is tagged as 3.10.4. Tags can be any arbitrary test, but it's conventional to assign a version number here. You'll also see different builds of the same version with tags like ":base_image-version_of image" or ":alpine-v2" for example, to indicate this image was based on alpine linux and is version 2 of our image. Later in the demo we'll see that other versions of python can be used at the same time.

1. On the next line, We set the path to which all subsequent commands will be relative. It's possible to change this later in the file by using the `WORKDIR` directive again. Dockerfiles are interpreted in order from the top to the bottom.

1. The next three lines do the work of copying local files into the imae and installing the libraries called for in `requirements.txt`. 

1. Finally the line beginning with `CMD` sets the default command that will run inside this container. In this case, we simply call our scirpt. There is another command `ENTRYPOINT` which works very similarly to `CMD`. The difference between them is that anything we set with `CMD` can be overwritten on the command line when we create a container based on this image. Whereas, `ENTRYPOINT` cannot be overwritten. If we use `ENTRYPOINT` and still pass options in extra parameters on the command line, they will be interpreted as arguments appended to whatever we set in `ENTRYPOINT`. If we set both `ENTRYPOINT` and `CMD` then the contents of `CMD` will be used as parameters passed to `ENTRYPOINT` and anything we pass on the commandline will overwrite the contents of `CMD`.

We build this container by changing into the `black-and-white` directory and issuing the following command:

```
docker build -t blackandwhite .
```

This simple command will build our image and give it the name black and white. Breaking it down, the command goes like this:

| | |
|-|-|
| docker | This calls the docker binary. |
| build | tells docker we want to access the "build" subcommand |
| -t | Assigns a name and a tag to our image. Normally it would be best practice to add a tag, such as 'v1' or something like it to our image. By not specifying a tag, docker will automatically use the tag "latest". This is fine for our demo but normally we should specify our own tag. |
| . | this is the path, in this case the current directory, where docker should look for all the relevant files to build our image |

This image builds quickly, but it is worth watching for the following:
- Since we don't currently have the python:3.10.4 image present on our system, docker will download all of the relevant layers.
- We can follow in the command output the progress as the commands we entered in the Dockerfile are executed.
- Should any of the commands in the Dockerfile fail the image will not be built.

After the container is built we can verify it is present on our system with the command:
```
docker images
```

This will produce output like the following.
```
REPOSITORY                  TAG             IMAGE ID       CREATED        SIZE
blackandwhite               latest          ddbb79a7d076   1 minute ago    938MB
```

Once our image is created we can instantiate it with:

```
docker run --rm \
    --mount type=bind,source="/path/to/image",target="/DATA" \
    -e IN_FILE='/DATA/in_file.jpg' \
    -e OUT_FILE='/DATA/out_file.jpg' \
    blackandwhite
```
Breaking that command down we get:
| | |
|-|-|
| docker | Like before we are calling the docker binary |
| run | Here we are calling the 'run' sub command to docker. This subcommand is responsible for instantiating a container based on an existing image. |
| --rm | This is an optional parameter that tells docker to remove the container from the system once it completes execution. Some times it is beneficial to let the exeted container remain on the system to allow for analyzing logs or resuming the container.
| --mount  | This flag tells docker that we want to mount part of the local filesystem into the container. Breaking this down further: <table><tr><td>type=bind</td><td>Tells docker what type of mount we want. Other types of mounts are outside of the scope of this demo; but could include named volumes, nfs shares, etc.</td></tr><tr><td>source="/path/to/image"</td><td>This is the source location on the local machine's file system that we want to mount into the container</td></tr><tr><td>target="/DATA"</td><td>This is the path __inside__ the container where we want to find the mounted file or directory.</td></tr></table> | 

>In the `workflow` directory there are helper scripts to run each container during the live demo. These scripts can be use outside of the live demo but may require modification, specifically to the pathnames, to work on other systems.

Running the container will result in a new file named `out_file.jpg` being created in the local filesystem at the location specified in our `--mmount` parameter above. 


## The containers

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