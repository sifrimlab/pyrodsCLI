# pyrodsCLI: improving command-line control of iRODS using their python-client

This repository contains a collection of scripts that utilize the iRODS python client to provide increased functionality. 

*Author:* David Wouters

*Contact:* david.wouters@kuleuven.be

## Dependencies

- python 3.6 or above
- json
- python-irodsclient

Optional for intelligent metadata generation:
- scikit-image

## Installation
<span style="color:red">This repository isn't pypi buildable yet!</span>
- Install with pip
```bash
pip install pyrodsCLI
```
- Use a conda environment:

```bash
conda env create -f conda.yml-p ./conda_env/ 
```

## Usage
After installation, the tool can be used as any other command-line interface.
Its options can be discovered by running the typical ```pyrodsCLI -h```.



