#!/bin/bash

docker run \
--rm \
--mount type=bind,source="/home/hudson/Projects/container-demo/DATA",target="/DATA" \
-e IN_FILE='/DATA/stage3.jpg' \
-e OUT_FILE='/DATA/stage4.jpg' \
vignette