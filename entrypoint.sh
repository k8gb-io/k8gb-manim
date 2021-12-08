#!/bin/bash

cd /workspace
manim $@
gif=$(find . -name "*.gif")
echo "::set-output name=gif_path::$video"