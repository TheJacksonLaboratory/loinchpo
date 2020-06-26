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