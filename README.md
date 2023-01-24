[![PyPI version](https://badge.fury.io/py/loinchpo.svg)](https://badge.fury.io/py/loinchpo) 
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/loinchpo/badges/version.svg)](https://anaconda.org/conda-forge/loinchpo)
![Alt text](./docs/coverage.svg)
# loinchpo
A simple and efficient library for mapping loinc test results to hpo terms.

Documentation: https://thejacksonlaboratory.github.io/loinchpo/
## Requirements
Python 3.5+

## Installing with pip

```bash
pip install loinchpo
```

## Installing with Conda

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install loinchpo
```




## Usage

Just three steps and you should be able to map your loinc codes to hpo.

### 1. Parse the annotations using AnnotationParser
A dictionary from file:
```python
annotations = AnnotationParser.parse_annotation_file(annotation_path)
```
A list from file:
```python
annotations = AnnotationParser.parse_annotation_file(annotation_path, ls=True)
```
A dictionary from pandas df:
```python
annotations = AnnotationParser.parse_annotation(dataframe)
```

### 2. Parse the query files
File path returns a list of queries:
```python
queries = QueryFileParser.parse(query_path)
```
Single query:
```python
query = Query(loinc_id, outcome)
```
### 3. Resolve the hpo term
```python
resolver = QueryResolver(annotations)
hpo_term = resolver.resolve(query)
```
