# <project-name>
![CI Pipeline](https://github.com/calgaryml/pytorch-poetry-hydra-template/actions/workflows/ci.yaml/badge.svg)
![CD Pipeline](https://github.com/calgaryml/pytorch-poetry-hydra-template/actions/workflows/cd.yaml/badge.svg)


## Repository Structure
...

## Installation
This project was developed using Python version >=3.10 and uses `poetry>=1.8.1` to manage dependencies and build the project. 

## Virtual Env
  ...

## Docker
For reproduction and instantiating replica's during training / inference, please use `Dockerfile` to build the image. Alternatively, you can pull the image from [Docker Hub](https://hub.docker.com/repository/docker/mklasby/condensed-sparsity). A large shm-size is required for pytorch to train ImageNet as this directory is used by the dataloader workers

### Development Container
For development, we recommend using vscode's devcontainer functionality to build and launch the development container. A `devcontainer.json` schema is provided in `./.devcontainer/` and if the project working directory is opened in vscode, the application will prompt the user to reopen in the development container. Please refer to the `devcontainer.json` schema and `Dockerfile.dev` for specifics on the development container environment and build process. 

To get started, please complete the following steps before reopening the workspace in the devcontainer:
* Copy the `.env.template` file to your own `.env` environiment file and edit it to add environmental variables. Without the `.env` file the dev container will not start.
* Create a directory `/datasets` and place any datasets you want to use (except for CIFAR-10) in that location. Alternatively, edit the mount directories in `./.devcontainer/devcontainer.json`
* Run `git submodue update` to pull from `cocoapi` third party repo. Migrate to ./src/cocoapi/PythonAPI and run `make && make install`

## Compute Canada
Compute Canada pre-builds many python packages into wheels that are stored in a local wheelhouse. It is best practice to use these wheels rather than use package distributions from PyPI. Therefore, the dependencies pinned in `pyproject.toml` have been carefully selected to ensure that the project enviornment can be replicated using the Compute Canada wheels that will match a local enviornment using PyPI package distributions. 

For simplicity, a bash script for installing the project and dependencies is included, see: `./scripts/build_cc_venv.sh`. Simply run this script from the project working directory after cloning the project from github. 

## Tests
This repository uses `pytest`.

Run tests using `pytest`
