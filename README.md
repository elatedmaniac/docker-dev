# README

## Overview

This project is aimed at creating a local, Dockerized environment for ML and DevOps projects. In order to maintain a robust security posture, I intend to integrate +1 of the following: [Renovate](https://github.com/renovatebot/renovate), [DependaBot](https://github.com/dependabot/dependabot-core), [Trivy](https://github.com/aquasecurity/trivy), and [Copa](https://github.com/project-copacetic/copacetic)

## Running the Environment

```bash
docker-compose run --build
```

### Endpoints

- Ollama: `curl -X POST http://localhost:11434/api/generate -d '{ "model": "phi3:medium", "prompt": "What is the capital of Zimbabwe?" }'`
  - Running a new model: `docker exec -it ollama ollama run llama3`
- Neo4j: `http://localhost:7474` (default http endpoint)

## References

### General Dev References

- .gitignore from GitHub: https://github.com/github/gitignore/tree/main
- Create an [automatically updating CHANGELOG](https://mokkapps.de/blog/how-to-automatically-generate-a-helpful-changelog-from-your-git-commit-messages)
- CloudFlared registry key on Windows host: [HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Application\Cloudflared]
- To get the dependencies for a particular Python module: `pip show <module_name>`
- Creating new certificates for TLS: `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./Nginx/certificates/dev.elatedmaniac.io.key -out ./Nginx/certificates/dev.elatedmaniac.io.crt -subj "/C=GR/ST=Attica/L=Athens/O=Olympus/OU=Gods/CN=dev.elatedmaniac.io"`  
- Using Mermaid in Drawio: https://www.drawio.com/blog/mermaid-diagrams
- [Converting fonts to other formats](https://transfonter.org/)
- [Button styling](https://uiverse.io/cssbuttons-io/friendly-dragon-76)
  
### Security

- OAuth + Jupyter: https://tljh.jupyter.org/en/latest/howto/auth/google.html

### Networking

- Explanation of Nginx as a reverse-proxy: https://medium.com/globant/understanding-nginx-as-a-reverse-proxy-564f76e856b2
- HTTP/2 in Nginx: https://www.tutorialspoint.com/how-to-enable-http2-0-in-nginx

### ML/ AI Datasets and Things I Found Helpful

- [StackOverflow dataset](https://archive.org/details/stackexchange)
- [AI profile search platform](https://theresanaiforthat.com/)
- [Ollama Modelfile parameters](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#parameter)
  
### Docker Images

- [Draw.io](https://hub.docker.com/r/jgraph/drawio)
- [Nginx](https://hub.docker.com/_/nginx)
- [Neo4J](https://hub.docker.com/_/neo4j)
- [Nvidia CUDA & Jupyter](https://hub.docker.com/r/nvidia/cuda)
- [Ollama](https://hub.docker.com/r/ollama/ollama)
- [Trivy](https://hub.docker.com/r/aquasec/trivy)