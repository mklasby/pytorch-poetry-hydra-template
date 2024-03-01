import pathlib
import re
from typing import Dict
import functools

_TARGETS = {
    "<name>": "name",
    "<email>": "email",
    "<drac-account>": "DRAC Account (def-xxxx)",
    "<working-dir>": "working directory",
    "<package-name>": "package name",
    "<repo>": "project repo on github",
    "<wandb-project>": "wandb project",
    "<wandb-entity>": "wandb entity",
    "<working-dir>": "working directory",
}

_SKIP_DIRS = {
    ".git",
    "data",
    ""
}

_SKIP_FILES = {
    ".env.template",
    "init_proj.py"
}

def patch_token(match, inputs):
    return inputs[match.group(0)]

def patch_file(child, inputs):
    if child.name in _SKIP_FILES:
        return
    with open(child, "r") as handle:
        file_text = handle.read()
        for k in inputs.keys():
            re.sub(k, functools.partial(patch_token, inputs=inputs), file_text)
        
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

def get_inputs():
    inputs = {}
    for k,v in _TARGETS.items():
        inputs[k] = input(f"Please input your {v}: ")
    inputs["<workspaceFolder>"] = inputs["<working-dir>"]
    print(f"You inputted: ")
    for k,v in inputs.items():
        print(f"{k}: {v}")
    is_correct = input(f"Is this correct? y/n")
    if is_correct.lower() == "y":
        return inputs
    else:
        get_inputs()

def main():
    inputs = get_inputs()
    walk_dir(pathlib.Path.cwd(), inputs)
    return

if __name__ == "__main__":
    main()
