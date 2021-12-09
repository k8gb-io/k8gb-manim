#!/bin/bash

cd /workspace
manim $@
echo -e "\n\nResults:"
tree ./media
gif=$(find ./media -name "*.gif")
echo -e "\n\nFound following gif file:"
ls -lh $gif
cp $gif /github/workspace/example/k8gb.gif
echo -e "\n\nIt was copied to:"
ls -lh /github/workspace/example/k8gb.gif
# ls -lh ./media/videos/k8gb/*/partial_movie_files/FailOver/
echo "::set-output name=gif_path::$gif"
