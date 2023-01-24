### Setup
```bash
pip install .[docs]
```

### Releasing
- Update version in __init__.py
- Run tests ```coverage run -m unittest discover loinchpo```

- Generate coverage report badge
### Building

#### PyPi
```bash
    python -m build
```

#### Deploying
```bash
python -m twine upload dist/*
```
To Conda:
- Update pypi hash/version
```bash
# https://conda-forge.org/#contribute
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