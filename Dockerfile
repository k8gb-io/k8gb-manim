FROM manimcommunity/manim:v0.12.0
COPY . /workspace
COPY entrypoint.sh /entrypoint.sh
WORKDIR /workspace
USER root
ENTRYPOINT ["/entrypoint.sh"]
