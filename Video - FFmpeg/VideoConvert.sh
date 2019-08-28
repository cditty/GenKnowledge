#!/bin/bash

# Clear the screen
clear

# Config Settings
# Converted file save location
mediaSaveDir=/Users/cditty/Desktop/Videos

# Path to file
FILEPATH=/Users/cditty/Desktop/Videos

# Getting filename for use
FILENAME=$(echo $1 | cut -f1 -d'.')
FILEEXT=$(echo $1 | cut -f2 -d'.')
FILEEXT=$(echo "$FILEEXT" | tr '[:upper:]' '[:lower:]')

if [[ $FILEEXT = "wmv" ]]; then
	echo "Please convert this to a mp4 format using Handbreak"
	exit 1
	else
	# Need to create a directory for video files
	if [ ! -d $mediaSaveDir/$FILENAME ]; then
  		mkdir -p $mediaSaveDir/$FILENAME;
	fi

	# Need to convert the video files now
	ffmpeg -i $FILEPATH/$1 -profile:v baseline -level 3.0 -s 640x360 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls $mediaSaveDir/$FILENAME/$FILENAME.m3u8

	# Need to do a screengrab
	ffmpeg -y -ss 1:45 -i $FILEPATH/$1 -vframes 1 -q:v 2 $mediaSaveDir/$FILENAME/$FILENAME.jpg

	# Coversion done - Time to move the file over
	cp $1 $mediaSaveDir/$FILENAME/$FILENAME.mp4
fi

