#!/bin/bash

## GET RESOURCES ##

# SBATCH --job-name=build-venv
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G    
#SBATCH --time=1-12:00:00
#SBATCH --mail-user=<<email>>
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --account=<<drac-account>>

## RUN SCRIPT ##
./scripts/build_drac_venv.sh
