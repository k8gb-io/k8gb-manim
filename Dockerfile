FROM manimcommunity/manim:v0.12.0
COPY . /workspace
COPY entrypoint.sh /entrypoint.sh
WORKDIR /workspace
# https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#docker-container-filesystem :
# Note: GitHub Actions must be run by the default Docker user (root)
USER root

RUN apt update && apt install -y tree && rm -rf /var/lib/apt/lists/* && apt clean && chmod -R 775 /workspace
ENTRYPOINT ["/entrypoint.sh"]
