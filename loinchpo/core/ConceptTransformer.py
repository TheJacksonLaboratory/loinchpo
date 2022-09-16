import pyspark.sql.functions as F


class ConceptTransformer:

    def obtains_loinc_scale_types(self, concept, concept_synonym, vocabulary):
        """Obtains all loinc concepts and parses their concept synonyms to obtain scale types."""

        df = self.preprocess_concepts(concept)

        # vocabulary provenance - combine vocabulary_name and vocabulary_version into single column
        vocabulary = vocabulary.na.fill(value="")
        vocabulary = vocabulary.withColumn("vocab_version",
                                           F.concat(F.col("vocabulary_id"), F.lit(" - Version "),
                                                    F.col("vocabulary_version")))
        # merge merged with measurement concepts and drop unneeded columns
        df_vocab_merge = df.join(vocabulary, ["vocabulary_id"], "left")
        drop_cols = (
            "vocabulary_id", "vocabulary_concept_id", "vocabulary_version", "vocabulary_name", "vocabulary_reference")
        df_vocab_merge = df_vocab_merge.drop(*drop_cols).dropDuplicates()

        # concept_synonyms - filter out non-english concepts and remove unneeded columns
        concept_synonym = concept_synonym.filter(concept_synonym.language_concept_id == 4180186).drop(
            *["language_concept_id"])
        # aggregate synonyms by concept_id
        concept_synonym = self.aggregate_synonyms_by_concept(concept_synonym).drop(
            *["concept_synonym_name"]).dropDuplicates()
        # merge data with vocab data
        df_vocab_syn_merge = df_vocab_merge.join(concept_synonym, ["concept_id"], "left")

        # get loinc scale types
        df_vocab_syn_merge = df_vocab_syn_merge.na.fill(value="None").dropDuplicates()
        scale_type_helper_function = F.udf(lambda x: self.finds_loinc_scale_type(x))
        loinc_scale_types = df_vocab_syn_merge.select("*", scale_type_helper_function("synonym_list").alias(
            "loinc_scale_type")).dropDuplicates().select("concept_id", "concept_code", "concept_class_id",
                                                         "concept_name", "synonym_list", "loinc_scale_type",
                                                         "vocab_version")

        return loinc_scale_types

    def preprocess_concepts(self, df):
        """Filters the concept table to return only loinc concepts"""
        # filter and remove un-needed columns
        drop_cols = ("domain_id", "standard_concept", "valid_start_date", "valid_end_date", "invalid_reason")
        return df.filter((df.domain_id == "Measurement") & (df.vocabulary_id == "LOINC") &
                         (df.invalid_reason.isNull())).drop(*drop_cols)

    def aggregate_synonyms_by_concept(self, df):
        """Aggregates synonyms by concept as a comma-delimited string"""

        # aggregate synonyms by concept_id
        df = df.na.fill(value="None").dropDuplicates()
        df = df.groupBy("concept_id").agg(F.collect_list("concept_synonym_name").alias("synonym_list")).dropDuplicates()

        # convert aggregated list to string and make lowercase
        df = df.withColumn("synonym_list", F.lower(F.array_join("synonym_list", ",")))

        return df

    def finds_loinc_scale_type(self, x):
        """Helper function for returns_loinc_scale_type that returns loinc scale type.
        Scale types selected from: https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#type-of-scale-5th-part"""

        if "quantitative" in x and "ordinal" in x:
            scale = "OrdQn"
        elif "ordinal" in x:
            scale = "OrdQn"
        elif "quantitative" in x:
            scale = "Qn"
        elif "nominal" in x or "qualitative" in x:
            scale = "Nom"
        elif "narrative" in x:
            scale = "Nar"
        elif "doc" in x:
            scale = "Doc"
        elif "set" in x:
            scale = "Set"
        elif "multi" in x:
            scale = "Multi"
        elif "panel" in x or "pnl" in x or "panl" in x:
            scale = "Pnl"
        else:
            scale = "Other"

        return scale
