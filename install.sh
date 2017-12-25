#!/bin/sh
#  检查aplay 即sox libsox-fmt-mp3     run:brew install sox  --with-lame on mac
if ![ -n `which play`]; then
 echo 'brew does not exist'
fi