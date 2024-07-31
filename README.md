# README

## Overview
This project is aimed at creating a local, Dockerized environment for ML and DevOps projects. In order to maintain a robust security posture, I intend to integrate +1 of the following: [Renovate](https://github.com/renovatebot/renovate), [DependaBot](https://github.com/dependabot/dependabot-core), [Trivy](https://github.com/aquasecurity/trivy), and [Copa](https://github.com/project-copacetic/copacetic)

## Running the Environment

```bash
docker-compose run --build
```

## References

### General Dev References

- .gitignore from GitHub: https://github.com/github/gitignore/tree/main
- Create an [automatically updating CHANGELOG](https://mokkapps.de/blog/how-to-automatically-generate-a-helpful-changelog-from-your-git-commit-messages)

### Networking

- Explanation of Nginx as a reverse-proxy: https://medium.com/globant/understanding-nginx-as-a-reverse-proxy-564f76e856b2
- HTTP/2 in Nginx: https://www.tutorialspoint.com/how-to-enable-http2-0-in-nginx

### ML/ AI Datasets and Things I Found Helpful

- StackOverflow dataset: https://archive.org/details/stackexchange

### Docker Images

- Draw.io: https://hub.docker.com/r/jgraph/drawio
- Nginx: https://hub.docker.com/_/nginx
- Neo4J: https://hub.docker.com/_/neo4j
- Nvidia CUDA & Jupyter: https://hub.docker.com/r/nvidia/cuda
- Ollama: https://hub.docker.com/r/ollama/ollama
- Trivy: https://hub.docker.com/r/aquasec/trivy