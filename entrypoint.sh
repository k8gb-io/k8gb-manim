#!/bin/bash

cd /workspace
manim $@
tree ./media
gif=$(find ./media -name "*.gif")
ls -lh $gif
cp $gif /github/workspace/example/k8gb.gif
ls -lh /github/workspace/example/k8gb.gif
echo "::set-output name=gif_path::$gif"
echo "$gif"