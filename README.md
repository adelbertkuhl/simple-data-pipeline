# simple-data-pipeline (current equity price data)

This project is an example of a simple data pipeline that runs on the Google Cloud Platform.

The pipeline consists of the following steps:

- REST API calls to [IEX Cloud financial data platform](https://iexcloud.io/), retrieving the latest equity price for UBER technologies at incremented intervals of 60 seconds.
- Publishing the ticker, price, and timestamp data to a Google Pub/Sub Topic
- An Apache Beam pipeline that retrieves the API data from the Google Pub/Sub Topic, cleans and transforms the published messages, and then loads them into a BigQuery table on GCP.

