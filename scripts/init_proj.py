import os
import pathlib
import re
import subprocess
from typing import Dict
import functools

_TARGETS = {
    "<<name>>": "Name for git config",
    "<<email>>": "Email for git config and/or slurm begin/end/fail notices",
    "<<drac-account>>": "DRAC Account (def-xxxx)",
    "<<working-dir>>": "Full path to working directory",
    "<<project-name>>": "Name of project and python package",
    "<<repo-url>>": "The URL of the project on github",
    "<<wandb-project>>": "wandb project",
    "<<wandb-entity>>": "wandb entity",
    "<<wandb-api-key>>": "wandb API key",
}

_TEMPLATE_CONFIG = {
    "<<poetry-version>>": "1.8.1",
    "<<user>>": os.environ["USER"],
    "<<uid>>": os.geteuid(),
    "<<gid>>": os.getegid(),
}

_SKIP_DIRS = {
    ".git",
    "data",
}

_SKIP_FILES = {".env.template", "init_proj.py"}


def patch_token(match, inputs):
    return inputs[match.group(0)]


def patch_file(child, inputs):
    if child.name in _SKIP_FILES:
        return
    with open(child, "r") as handle:
        file_text = handle.read()
        for k in inputs.keys():
            file_text = re.sub(
                k, functools.partial(patch_token, inputs=inputs), file_text
            )
    with open(child, "w") as handle:
        handle.write(file_text)
        handle.flush()
    return


def walk_dir(dir: pathlib.Path, inputs: Dict[str, str]):
    if dir.name in _SKIP_DIRS:
        return
    for child in dir.iterdir():
        if child.is_dir():
            walk_dir(child, inputs)
        elif child.is_file():
            patch_file(child, inputs)
        else:
            raise RuntimeError("Not a dir or a file!?")


def generate_env_file():
    subprocess.run(["cp", ".env.template", ".env"])


def get_inputs():
    inputs = {}
    for k, v in _TARGETS.items():
        inputs[k] = input(f"Please input your {v}: ")
    # We don't want extra dir delimiter in working-dir
    inputs["<<working-dir>>"] = inputs["<<working-dir>>"].rstrip("/")
    print(f"You inputted: ")
    for k, v in inputs.items():
        print(f"{k}: {v}")
    is_correct = input(f"Is this correct? y/n: ")
    if is_correct.lower() == "y":
        inputs.update(_TEMPLATE_CONFIG)
        return inputs
    else:
        get_inputs()


def main():
    inputs = get_inputs()
    generate_env_file()
    walk_dir(pathlib.Path.cwd(), inputs)
    return


if __name__ == "__main__":
    main()
