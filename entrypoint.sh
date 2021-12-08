#!/bin/bash

cd /workspace
manim $@

tree ./media
gif=$(find ./media -name "*.gif")
cp $gif /github/workspace/k8gb.gif
echo "::set-output name=gif_path::$gif"
echo "$gif"