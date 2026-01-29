FROM jenkins/jenkins:latest-jdk21
USER root

RUN apt update && apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release


RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null


RUN apt update && \
    apt install -y docker-ce-cli docker-compose-plugin

USER jenkins
