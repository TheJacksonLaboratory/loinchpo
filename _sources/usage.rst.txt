====================================
Using LoincHPO
====================================

**Simple Use Case**
-------------------

#. Parse the annotations from (https://github.com/TheJacksonLaboratory/loinc2hpoAnnotation)  using AnnotationParser::

    # If you loaded the annotations into a pandas df:
    annotations = AnnotationParser.parse_annotations(dataframe)

    # If you simply have the file:
    annotations = AnnotationParser.parse_annotation_file(annotation_path)


#. Create your queries::

    # From a file:
    queries = QueryFileParser.parse(query_path)
    # A single query:
    query = Query(loinc_id, outcome)

#. Resolve the hpo term::

    resolver = QueryResolver(annotations)
    hpo_term = resolver.resolve(query)


**OMOP Common Data Model** (Requires Spark)
-------------------------------------------

For a more detailed description on the way we transform OMOP measurements to Human Phenotype Ontology terms :ref:`visit here <omop>`.
You will need the major tables **Concept**, **Concept Synonym**, **Measurement**.

If you have the tables in a file format use::

        parser = ClinicalTableParser()
        concept = parser.parse_table("/some/file/path", ClinicalTableName.CONCEPT, your_spark_session)
        ... the 2 other tables
        df = OMOPTransformer.transform(concept, concept_synonym, measurement)

If you have the tables in spark df already::

        df = OMOPTransformer.transform(concept, concept_synonym, measurement)


