#!/bin/bash

# Older style volume mount.
# -v "/home/hudson/Projects/container-demo/DATA":"/DATA":Z \

docker run \
--rm \
--mount type=bind,source="/home/hudson/Projects/container-demo/DATA",target="/DATA" \
-e IN_FILE='/DATA/image.jpg' \
-e OUT_FILE='/DATA/stage2.jpg' \
blackandwhite