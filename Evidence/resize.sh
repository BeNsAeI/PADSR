#!/bin/bash
for i in {1..16}
do
	convert $i.jpg -resize 640x420\> $i.jpg
done
