# IMX Dev Ops/SRE take home challenge

## Intoduction
Thank you for taking your time to interview with IMX!! For this portion of the interview process, we ask that you complete the challenge in this repository as outlined below. Please give it your best shot! 

If something is giving you trouble, always feel free to reach out to the IMX team for clarification.

Your time is unlimeted, but we anticipate this task to take less than 3 hours. If you feel like the task is taking an inordinate amount of time, feel free to stop and discuss the details with us in the debreif!

## The Application
The challenge centers around performing some Dev Ops tasks related to the application in this repository, the Claims API. The Claims API is a restful API that provides information about healthcare claims from a database.

The API is written for python 3.11 and dependencies for the application are included in the requirements.txt file in the repoistory root.

## Challenge 1: Dockerfile
The Claims API has is ready to be deployed into UAT for testing, however it's Dockerfile is incomplete! Complete the dockerfile for the application with these considerations in mind:

1. The application uses data stored in `/opt/claims-api/` that is expected to be mounted at runtime
2. The application should be run from /claims-api in the root of the docker container

## Challenge 2: Helmfile
This application will be deployed in a kubernetes cluster. We need a helmfile to define it's configuration. Create a helm template that satisfies the following requirements:

1. Create the chart in a folder called `chart` in the repo root
2. The API will be publicly exposed to the internet
3. The API needs some directories to be present to run
   1. it needs the data sources mounted in `/opt/claims-api/`
   2. There is a public and private key in the `/keys` directory of this repo, the application needs them at a different mount point
   _NOTE_: Storing these keys in the repo root is certainly not a good idea, but you can ignore it for the purposes of this exercise.
4. The default value for the CLAIMS_API_PORT should be 9950

## Challenge 3: Github Actions
Now that we have the Dockerfile and Helm chart, we need to add the CI/CD pipeline for the API. Add a github action with the following requirements:

1. For pull requests:
   1. Build the Dockerfile
   2. Run the application tests using pytest in the built docker container using pytest
      1. To do this, the 'python -m pytest' command needs to be run in the app directory
   3. Build the Helm Chart
2. When the pull request is merged into main:
   1. Buld the dockerfile
   2. Run the application tests
   3. Push the dockerfile to the docker repository to the latest tag (Bonus: also push to a version tag of some kind.)
   4. Push the helm chart to the repository 

_NOTE_: for the push portion of the execcise, feel free to push to your personal docker repo.

