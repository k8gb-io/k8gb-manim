# k8gb animations

These animations use the Manim [community version](https://www.manim.community/) of the library ([code](https://github.com/ManimCommunity/manim)),
you can install it by following the instructions for your OS on their web site.

## Rendering the animations

```bash
# for development
manim k8gb.py -pql

# for high-quality video
manim k8gb.py -qk

# for high-quality gif
manim k8gb.py -gh --format=gif
```

## Example

![k8gb simple animation](https://github.com/jkremser/k8gb-manim/raw/master/example/k8gb.gif)

### Up-to-date version in lower quality

rendered with 10fps and low-quality(480p):
![k8gb simple animation(low-q)](https://github.com/jkremser/k8gb-manim/raw/master/example/k8gb-low-q.gif)

This low-quality version of gif is being updated by the gh action in this repo.