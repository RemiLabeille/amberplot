# amberplot

AMBER MD trajectory analysis and plotting tools

## Features

- Parse AMBER MD output files (.out)
- Generate system variable plots
- Extract trajectory frames to individual PDB files
- Batch processing with command-line arguments

## Installation

### Requirements
- Python 3.11+
- conda or pip

### Setup

```bash
conda create -n amberplot -c conda-forge python=3.11 pandas matplotlib netcdf4 mdtraj
conda activate amberplot
pip install -e .