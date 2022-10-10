#!/bin/bash
IN_FILE=$(pwd)/../DATA/stage5.jpg
echo $IN_FILE
ls -l ${IN_FILE}
docker cp ${IN_FILE} portfolio-web:/usr/share/nginx/html/images/final.jpg