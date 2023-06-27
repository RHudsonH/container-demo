# Container Demo

These are the demonstration files that accompany an Intruduciton to Containers. Which is a webinar presented as a part of the Mark III Education series.

The webinar begins with a brief set of slides found in `Container Basics.pptx` and then transitions to a live demo.

During the live demo, we walk through a series of very similar containers that serve to show the basics of containerizing a workflow, accessing data from withing a running containers and saving files out of the containers. We start with the `black-and-white` directory.

## Black and white.
---

This being the first container, we will thorougly explore the directories contents.

### 1. `blackandwhite.py`
This file contains a simple python script that will open the file specified int the environment variable `IN_FILE`, convert the image to black and white and then save the file out to the location specified in another environment variable named `OUT_FILE`.

This script uses environment variables to set the required parameters. However, we could have use command line parameters which could be passed to docker when we create the container.   

### 2.  `requirements.txt`
This file lists the library requirements for the script `blackandwhite.py`. There's only one line here as there is only one required non-standard python library. 

### 3. `Dockerfile`
The file that will instruct `docker` on how to build the image we want to run our script. 

In looking through this file it is helpful to point out a number of things that are helpful to understand as the demo progresses.
 
1. On the line that begins with `FROM` we are specifing the base container that we will be building on. This base image was chosen as it provides a jummping off point that is close to what we want our final image to look like. We could start with some other base image. For example if we wanted to start with an image that didn't already have python installed, we could do so, but then we would have to make sure to include all of the necessary commands to install python. This could allow us to do a custom build of python.

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
    -e IN_FILE='/DATA/stage1.jpg' \
    -e OUT_FILE='/DATA/stage2.jpg' \
    blackandwhite
```
Breaking that command down we get:
| | |
|-|-|
| docker | Like before we are calling the docker binary |
| run | Here we are calling the 'run' sub command to docker. This subcommand is responsible for instantiating a container based on an existing image. |
| --rm | This is an optional parameter that tells docker to remove the container from the system once it completes execution. Some times it is beneficial to let the exeted container remain on the system to allow for analyzing logs or resuming the container.
| --mount  | This flag tells docker that we want to mount part of the local filesystem into the container. Breaking this down further: <table><tr><td>type=bind</td><td>Tells docker what type of mount we want. Other types of mounts are outside of the scope of this demo; but could include named volumes, nfs shares, etc.</td></tr><tr><td>source="/path/to/image"</td><td>This is the source location on the local machine's file system that we want to mount into the container</td></tr><tr><td>target="/DATA"</td><td>This is the path __inside__ the container where we want to find the mounted file or directory.</td></tr></table> | 
| -e | This tells docker that we want to set an environment variable in the running container. We can call `-e` multpile times to set multiple environment variables. In this case we're calling it twice. The first time we set the input file to use, and the second time we set the name of the file we would like to create after the filter is applied. <table><tr><td>IN_FILE='/DATA/stage1.jpg'</td><td>The input file name. Here we used an absolute path /DATA is mounted in from our file system via the mount option.</td></tr><tr><td>OUT_FILE='/DATA/stage2.jpg'</td><td>The name of the file we want to create after applying the filter.</td></tr></table>|

> In the `workflow` directory there are helper scripts to run each container during the live demo. These scripts can be use outside of the live demo but may require modification, specifically to the pathnames, to work on other systems.

Running the container will result in a new file named `out_file.jpg` being created in the local filesystem at the location specified in our `--mmount` parameter above. 


## sepia
---

The next container we look at is in the `sepia` directory. This container is very similar to the Black and White one. There is a python script, requirements.txt file, and a Dockerfile. This time the script will apply a sepia look to the image that we select.

In the Dockerfile for this image we see that the base image called for with the `FROM` directive is `python:3.9.2`. This illustrates that it's trivial to have multiple versions of the same software running concurrently in different containers.

We build this one as before by changing into the `sepia` directory and running:

```
docker build -t sepia .
```

The only difference between this command and the one we ran for the blackandwhite container is the name after the `-t` flag. As the image builds we can see in the output that docker needed to pull the new base image for `docker:3.9.2`. 

Our run command is also nearly identical. This time we use the output of our previous container as the input of our new container.

```
docker run --rm \
    --mount type=bind,source="/path/to/image",target="/DATA" \
    -e IN_FILE='/DATA/stage2.jpg' \
    -e OUT_FILE='/DATA/stage3.jpg' \
    sepia
```

This one takes a short amount of time to run, but we have time to run:

```
docker ps 
```

Which will show us the containers that are currently running. The output should be similar to:

```
CONTAINER ID   IMAGE     COMMAND                 CREATED         STATUS         PORTS     NAMES
f3d6cdddef6e   sepia     "python ./img2sep.py"   5 seconds ago   Up 4 seconds             dazzling_meitner
```

We can use either the `CONTAINER ID` or the `NAMES` to refer to our container in other docker commands. We can also see the command that was run inside the container matches what we had set in the Docker file. The name is automatically, randomly assigned by docker if none is specified. When we run the container we can specify any name we like as long as there are no other containers with the same name. We can also override the `command` by passing argumants _after_ the image name.

For example:
```
docker run -t -i -n my_python python:latest bash
```
would create a container nameed `my_python` based off of the latest version of the python image; and would give us a bash shell prompt. In this example, the `-t` and `-i` options work together to give us an **i**nteractive **t**erminal. This is often shortend to `-ti` in practice. The `-n` flag is how we pass in our desired container name.

## vignette
---

The next container in the series is `vignette`. Like `blackandwhite` and `sepia` before, this image consists of a python script, requirements.txt file and a Dockerfile. The script here applies a vignette to the image being processed.

This image is built and run in the same way as our previous two. The Dockerfile for this one calls for a base image of `python:3.10.4` like `blackandwhite` did before. When this image is built the output will show that no additional layers are downloaded, because they've already been fetched during the building of `blackandwhite`. building this new image takes less disk space than the orriginal build of `blackandwhite` did. This is because both images use the same base image. When a new image is built from a base image, the commands we issue in the Dockerfile are built as read only layers that are stacked on the base image.

In fact, if we looked into the `python:3.10.4` base image shared shared by both `blackandwhite` and `vignette` we would find that it was built on some other base image.

We can see this in our two images if we inspect them:

```
$ docker inspect blackandwhite:latest  | jq '.[].RootFS.Layers[]'
"sha256:e7597c345c2eb11bce09b055d7c167c526077d7c65f69a7f3c6150ffe3f557ea"
"sha256:7dbadf2b9bd82a7447533776d0c8de6687cfcf241d3aa993ed8a86ad1347c6e0"
"sha256:9177197c67d08b25357b0b5ba8f7b944f321970dddbbe93b36cb726e9bdfd678"
"sha256:ee509ed6e976cdad5adda963902f78e442ea5fc05f955bd2c2c9026789f84b42"
"sha256:2fbabeba902e7f7c521f478f855b738d91bd4f2435de223a89fa5f4b2369065a"
"sha256:13b045a1dfd29f39dcb5ef608d2c2b82a5dd53eae4441985188dd77541011a96"
"sha256:9ea8d200cd5db04ba9393271fd606a54ead75068ecbd6827442bc9ba48507a64"
"sha256:428e1f341db71cae5e06d264b527a1591adb54869621c4d7716f9c8706b663f3"
"sha256:9fda40ddc568d136d5b0f137e766c81535fbc924c587f0163c1e1aca5abe0402"
"sha256:80f0eed168636d2fe02ecee0611c266217f5bff1af9e14d1a900820c005cfc92"
"sha256:7e18fb6c43f50ec60988d5540e058ab21d28f7feebadc322005e5559d098ac16"
"sha256:d6d86517af21cc2f8ed63e5354ea66e6361e7749db26292c4c6659abe6120810"
"sha256:fd7ebdf8537b687de69bc1c45121e8c4c099a43911611dc46b38955d2de514cd"
$
$ docker inspect vignette:latest  | jq '.[].RootFS.Layers[]'
"sha256:e7597c345c2eb11bce09b055d7c167c526077d7c65f69a7f3c6150ffe3f557ea"
"sha256:7dbadf2b9bd82a7447533776d0c8de6687cfcf241d3aa993ed8a86ad1347c6e0"
"sha256:9177197c67d08b25357b0b5ba8f7b944f321970dddbbe93b36cb726e9bdfd678"
"sha256:ee509ed6e976cdad5adda963902f78e442ea5fc05f955bd2c2c9026789f84b42"
"sha256:2fbabeba902e7f7c521f478f855b738d91bd4f2435de223a89fa5f4b2369065a"
"sha256:13b045a1dfd29f39dcb5ef608d2c2b82a5dd53eae4441985188dd77541011a96"
"sha256:9ea8d200cd5db04ba9393271fd606a54ead75068ecbd6827442bc9ba48507a64"
"sha256:428e1f341db71cae5e06d264b527a1591adb54869621c4d7716f9c8706b663f3"
"sha256:9fda40ddc568d136d5b0f137e766c81535fbc924c587f0163c1e1aca5abe0402"
"sha256:80f0eed168636d2fe02ecee0611c266217f5bff1af9e14d1a900820c005cfc92"
"sha256:335bfc73c876b3bd1d790eb58fb96180ba57fa5ab89786f182142df2068fd2ec"
"sha256:f1694a8e8a1bdc3fbc9c58a6b5994ea1d5461f5ea2604bc744b62153f22dd7ae"
"sha256:6ea55e2e11c6ca2f389c1f54128f97efe426f9361cd5fb4d5285ef33aace568e"
```

when a layer is created, It's assigned a name or id based on  a hash of it's contents. We can see above that our two images share 10 of their 13 layers. Those shared images are not duplicated on disk. They are stacked into a root filesystem for the container when the container is instantiated.

The three differing layers can be accounted for by the three commands in the Docerfile that would cause changes to a filesystem, In this case there are two `COPY`s and one `RUN` which installs some software.

## resize

We usually skip the resize image during the demo. It is almost identical to the others here but it resizes the image passed to it. If you run resize before the sepia container then sepia will complete much faster with less pixels to operate on.

## web

This image is being worked on to provide and introduction to orchestration in the future.


## Some Handy Commands
---
The following are just some handy commands that I find my self trying to remember. I put them here so I would know where to look for them next time I need them. I hope the help others too!

### Stop all docker containers
```
docker stop `docker ps --all | awk '{print $1}' | grep -v CONTAINER`
```
#### Stop all docker containers
```
docker rm `docker ps --all | awk '{print $1}' | grep -v CONTAINER`
```

#### Remove all docker images.
```
docker image rm `docker image ls --all | awk '{print $3}' | grep -v IMAGE`
```