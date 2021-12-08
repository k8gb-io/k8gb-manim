FROM manimcommunity/manim:v0.12.0
# COPY k8gb.py /
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
