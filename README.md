# simple-data-pipeline (Bitcoin exchange rate data)

This project is an example of a simple data pipeline that runs on the Google Cloud Platform.

The pipeline consists of the following procedures:

- REST API calls to [IEX Cloud financial data platform](https://iexcloud.io/), retrieving the latest Bitcoin (BTCUSDT) exchange rate at incremented intervals of 60 seconds.
- Publishing the ticker, exchange rate, and timestamp data to a Google Pub/Sub Topic.
- An Apache Beam pipeline that retrieves the API data from the Google Pub/Sub Topic, cleans and transforms the published messages, and then loads them into a BigQuery table on GCP.

### Detailed instructions

After loading the python modules and `setup.sh` script into Google Cloud Shell, execute the following command to kick off the process that publishes the exchange rate data to Pub/Sub from API REST calls:

```python publish.py```

You'll notice the publisher prints each API response to the console output, at the specified time increment (60 seconds).


![Image description](https://github.com/adelbertkuhl/simple-data-pipeline/blob/master/img/Screen%20Shot%202019-10-06%20at%206.13.50%20PM.png)


In another cloudshell tab, run the following command to kick off a new GCP DataFlow job:

```
python main_pipeline.py \
--runner DataFlow \
--project $PROJECT \
--temp_location $BUCKET/tmp \
--staging_location $BUCKET/staging \
--streaming
```

A new job dashbboard view will appear in the console. You can see each step of the pipeline in-progress and inspect successful or unsuccessful log reports. 


![Image description](https://github.com/adelbertkuhl/simple-data-pipeline/blob/master/img/Screen%20Shot%202019-10-06%20at%206.14.17%20PM.png)


The pipeline downloads the message data from the specified Google Pub/Sub topic and performs a set of cleaning and transformation operations. The data is loaded into a GCP BigQuery table at the last step of the pipeline.


![Image description](https://github.com/adelbertkuhl/simple-data-pipeline/blob/master/img/Screen%20Shot%202019-10-06%20at%206.14.45%20PM.png)

