#!/bin/bash

VIDEO_ID=$1
OUTPUT_DIR=$2

[ -z "$OUTPUT_DIR" ] && echo "ERROR: No output directory specified" && exit 1

[ -z "$VIDEO_ID" ] && echo "ERROR: No video ID specified" && exit 1

yt-dlp --no-playlist --extract-audio --audio-format wav --audio-quality 0 --output "$OUTPUT_DIR/%(title)s.%(ext)s" $VIDEO_ID
