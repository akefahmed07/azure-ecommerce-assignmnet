# Databricks notebook source
# Run once in a dedicated demo schema with no concurrent writers.
from pyspark.sql import functions as F
import re

dbutils.widgets.text("catalog", "")
dbutils.widgets.text("schema", "")
dbutils.widgets.text("source_volume_path", "")
catalog, schema, source = [dbutils.widgets.get(key).strip() for key in
                           ("catalog", "schema", "source_volume_path")]
if not all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s) for s in (catalog, schema)):
    raise ValueError("Enter a catalog and schema using letters, digits and underscores.")
if not source.startswith("/Volumes/"):
    raise ValueError("Set source_volume_path to the volume folder containing the four CSV files.")

for entity in ("customers", "orders", "order_items", "products"):
    path = f"{source.rstrip('/')}/{entity}.csv"
    target = f"`{catalog}`.`{schema}`.`bronze_{entity}`"
    batch = spark.read.option("header", True).csv(path)
    incoming = batch.count()
    before = spark.table(target).count() if spark.catalog.tableExists(target) else 0
    enriched = (batch.withColumn("source_file", F.lit(f"{entity}.csv"))
                     .withColumn("ingested_at", F.current_timestamp()))
    enriched.write.format("delta").mode("append").saveAsTable(target)
    after = spark.table(target).count()
    print(f"{entity}: before={before}, incoming={incoming}, after={after}")
    if after - before != incoming:
        raise ValueError(f"Row-count mismatch for {entity}")
