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

## Run the example in Azure Databricks

1. Use a Unity Catalog-enabled compute environment. Choose an existing catalog and a dedicated demo schema where you can create managed tables. Use a volume where you can upload and read files.
2. Upload [customers.csv](customers.csv), [orders.csv](orders.csv), [order_items.csv](order_items.csv) and [products.csv](products.csv) to the same volume folder. Each repository CSV contains 20 data rows plus its header.
3. Import the [Bronze ingestion notebook](notebooks/bronze_ingestion.py) as a Databricks source notebook. Run the cell to initialize its widgets, enter the catalog, schema and source folder (for example, `/Volumes/demo/retail/input`), then rerun the cell.
4. Read the printed before, incoming and after counts. Starting with empty targets, the expected result for each table is `before=0, incoming=20, after=20`. A second full run appends another 20 rows per table.

The example preserves source fields as strings and adds `source_file` and `ingested_at`. It writes `bronze_customers`, `bronze_orders`, `bronze_order_items` and `bronze_products`. Run one writer at a time. If a run stops midway, check the per-table counts before retrying because previously completed appends are already committed.
