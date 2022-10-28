import pyspark.sql.functions as F


class ConceptSynonymTransformer:

    def transform(self, df, concept, concept_synonym):
        """
            A function to attach synonyms to loinc concept_names.
        """
        language_concept = self.english_concept_synonym_filter(concept_synonym, concept.select("concept_id", "concept_name").dropDuplicates())
        concept_synonym = concept_synonym.filter(concept_synonym.language_concept_id == language_concept.concept_id)
        concept_synonym = self.aggregate_synonyms_by_concept(concept_synonym).drop(
            *["concept_synonym_name"]).dropDuplicates()
        return df.join(concept_synonym, ["concept_id"], "left")

    def english_concept_synonym_filter(self, concept_synonym, concept):
        """
            Filter the concept table down to only the concepts that are in concept_synonym
            then join and find the english one
        """
        language_concept_ids = set(concept_synonym.select("language_concept_id").toPandas()["language_concept_id"])
        english = concept.where(F.col("concept_id").isin(language_concept_ids)).where(
            F.lower(F.col("concept_name")).contains("english"))
        return english.first()

    def aggregate_synonyms_by_concept(self, df):
        """
            Aggregates synonyms by concept as a comma-delimited string
        """

        df = df.na.fill(value="None").dropDuplicates()
        df = df.groupBy("concept_id").agg(F.collect_list("concept_synonym_name").alias("synonym_list")).dropDuplicates()
        df = df.withColumn("synonym_list", F.lower(F.array_join("synonym_list", ",")))
        return df
