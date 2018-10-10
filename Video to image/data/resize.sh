#!/bin/bash
#for i in {1..2893}
for i in {1..2893} 
do
	convert frame${i}.jpg -resize 600x400\> resized/frame${i}.jpg
	echo frame${i}.jpg resized
done
