====================================
Observational Medical Outcomes Partnership (OMOP) Common Data Model
====================================
"The `OMOP Common Data Model <http://https://www.ohdsi.org/data-standardization/the-common-data-model/>`_  allows for the systematic analysis of disparate observational databases.
The concept behind this approach is to transform data contained within those databases into a common
format (data model) as well as a common representation (terminologies, vocabularies, coding schemes),
and then perform systematic analyses using a library of standard analytic routines that have been written
based on the common format."

This common data model provides us with opportunity to transform LOINC concepts in OMOP to Human Phenotype Ontology
terms. We need three pieces of data that are important to transforming, the LOINC id, the LOINC scale type, and the value.

You will need the major tables *Concept*, *Concept Synonym*, *Vocabulary* and *Measurement*.

Identifying LOINC Data in OMOP
-----------------

#. Obtain LOINC Concept & Scale values [*Concept*, *Concept Synonym*, *Vocabulary*]
    * Filter the concept table by vocabulary for LOINC
    * Filter concept synonyms for english concepts only
    * Aggregate concept synonyms on concept_id creating a single cell for each concept with a synonym list
    * Iterate over synonym list for each concept to find the scale type ( should contain inference values )

#. Preprocess and impute Measurements for LOINC Concepts [*Measurement*, *Concept*]
    * Filter for measurements that contain LOINC concepts from the concept table
    * Remove measurement rows that have no values, dropping duplicate rows
    * Verify and impute data for concept codes that have negatives values expect for special concept codes (refer to OMOP CDM)
        * 3003396 (Base excess in Arterial blood by calculation)
        * 3002032 (Base excess in Venous blood by calculation)
        * 3006277 (QRS-Axis), 3012501 (Base excess in Blood by calculation)
        * 3003129 (Base excess in Capillary blood by calculation)
        * 3004959 (Base excess in Arterial cord blood by calculation)
        * 3007435 (Base excess in Venous cord blood by calculation)
#. Obtain measurements for LOINC Concepts
    * For numerical values we infer high, low, normal, from the reference range columns value_range_high, value_range_low, and the value itself
    * For categorical values we map known categorical results in value concept name::

        postive_results = ["positive", "detected", "abnormal", "yes"]
        negative_results = ["negative", "not detected", "normal", "acceptable", "healthy", "in range", "non-reactive",
                        "nonreactive", "none detected", "none seen", "not detected/negative", "not present", "no"]
    * For data that does not have valid numerical data or is missing range_high, range_low we flag these as bad values, but keep them for further analysis.

#. Compile Processed Patient Level Results
    * Join data from 1. Obtaining LOINC Concept & Scale values on 3. Obtain measurements by concept_id, concept_code, concept_name
    * Filter out marked bad loinc values from 3