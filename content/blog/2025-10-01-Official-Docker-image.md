+++
title = "Official Docker image"
+++

The Veryl team has published the official Docker image of Veryl.
It can be used as the base image for your custormized image, GitLab CI/CD and so on.

[https://hub.docker.com/r/veryllang/veryl](https://hub.docker.com/r/veryllang/veryl)

Additionally, this project was approved for ["Docker-Sponsored Open Source program"](https://www.docker.com/community/open-source/application/).
By collaborating with Docker Inc., unlimited pull rate is provided.

Here is some examples to use the Docker image.

## `docker` command

You can pull the docker image from `veryllang/veryl`.

```console
$ docker pull veryllang/veryl
```

## `Dockerfile`

If you want to use the official image as a base of your Docker image, the following `FROM` directive can be used.

```
FROM veryllang/veryl:latest
```

## GitLab CI/CD

The following is an example of `.gitlab-ci.yml` for [GitLab](https://gitlab.com) CI/CD.

```yaml
image: "veryllang/veryl"

build:
  stage: build
  script:
    - veryl build

fmt:
  stage: build
  script:
    - veryl fmt --check
```
