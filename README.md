# E-commerce ingestion with Azure Databricks

This project uses PySpark to ingest four e-commerce datasets into the Bronze layer of a Delta Lake. Customers, orders, order items and products each have their own destination table in Unity Catalog.

## Ingestion workflow

1. Read the source records for each dataset.
2. Add ingestion metadata so each batch can be traced after loading.
3. Append the records to the corresponding managed Delta table.
4. Check the destination row counts against the incoming batch.

The order items dataset captures the individual product lines within an order. Keeping it separate from orders preserves that distinction for later analysis.

## Validation

For an append load, compare the increase in the destination row count with the number of incoming rows. Replaying a previously loaded batch can append the same records again.
