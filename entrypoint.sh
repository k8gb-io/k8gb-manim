#!/bin/bash

manim $@
gif=$(find . -name "*.gif")
echo "::set-output name=gif_path::$video"