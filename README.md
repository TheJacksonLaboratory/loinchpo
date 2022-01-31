# loinchpo
A simple and efficient library for mapping loinc test results to hpo terms.

## Requirements
Python 3.5+

## Installing with pip

```bash
pip install loinchpo
```

## Installing with Conda

```bash
# Ensure conda-forge is in your channels
conda config --add channels conda-forge
conda config --set channel_priority strict

# Install the package
conda install loinchpo
```


## Usage

Just three steps and you should be able to map your loinc codes to hpo.

### 1. Parse the annotations using AnnotationParser
```python
    # returns a list of the annotations
    annotations = AnnotationParser.parse_annotation_file(annotation_path)
```
```python
    # returns a dictionary query mapper
    annotations = AnnotationParser.parse_annotation_file_dict(annotation_path)
```
```python
    # returns a dictionary query mapper from a pandas dataframe
    annotations = AnnotationParser.parse_annotation_pandas(dataframe)
```

### 2. Parse the query files
```python
    # file path returns a list of queries
    queries = QueryFileParser.parse(query_path)
```
```python
    # single query
    query = Query(loinc_id, outcome)
```
### 3. Resolve the hpo term
```python
    # Resolve the hpo term.
    resolver = AnnotationResolver(annotations)
    hpo_term = resolver.resolve(query)
```









