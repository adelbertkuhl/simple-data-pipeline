# simple-data-pipeline

This project consists of a simple data pipeline that runs on the Google Cloud Platform. 

The pipeline consists of the following steps:

- REST API calls to IEX Cloud financial data platform, retrieving at incremented intervals of 60 seconds the latest equity price for UBER technologies.
- Publishing the ticker, price, and timestamp data to a Google Pub/Sub Topic
- An Apache Beam pipeline that retrieves the API data from the Google Pub/Sub Topic, cleans and transforms the published messages, and then loads them into a BigQuery table on GCP.

