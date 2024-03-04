#!/bin/bash
# Converts main.py into a notebook for hacking
# probably need to update config location
jupytext --to notebook ./main.py -o ./notebooks/main.ipynb
