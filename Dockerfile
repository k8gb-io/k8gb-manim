FROM manimcommunity/manim:v0.12.0
COPY . /workspace
COPY entrypoint.sh /entrypoint.sh
WORKDIR /workspace
USER root

RUN apt update && apt install -y tree && rm -rf /var/lib/apt/lists/* && apt clean
ENTRYPOINT ["/entrypoint.sh"]
