## Contributing

#### With Conda

```bash
# Import the current conda env in the repository
conda env create -f envrionment.yml

# Activate the conda env
conda activate <name>

# If you update the environment aka installing packages, update the yml
conda env export > environment.yml
```

##### Building for conda-forge
```bash

# Set conda forge
conda config --add channels conda-forge
conda config --set channel_priority strict

# Will run tests and prepore for the forge
conda build conda_recipe

# Cleaning if you built many times, will clean the build directories
conda build purge 

# Installing recently built version
conda install --use-local loinchpo
```


#### Uploading to conda-forge
```bash
# https://conda-forge.org/#contribute
```

#### PyPi
```bash
    python3 setup.py sdist bdist_wheel
```

#### Deploying
```bash
    python3 -m twine upload dist/*
```