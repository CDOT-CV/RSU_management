#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pylint:disable=E1101

"""
This script handles the handling of data between the raw ingest, the data lake, and the
data warehouse. Furthermore, this script is one meant to be run locally, and was mainly designed
to demonstrate the data flow process between storage containers in the GCP. 
The raw ingest and data lake at present are located in their respective buckets in the GCP. 
The data warehouse is currently a Pub/Sub topic to which cleaned data will be published in byte string form.
"""

import json
import ndjson
import os
from google.cloud.storage import Client             # google cloud - storage / bucket access
from google.cloud.pubsub_v1 import PublisherClient  # google cloud - pub/sub topic access
import datetime
import logging
from string import Template

def is_json_clean(rsu_data):
    """
    Returns TRUE if json_file is clean. FALSE otherwise.
    Args: 
        rsu_data: RSU data as a list of dicts from raw ingest to be checked
    """
    isJSONclean = True
    
    #check: duplicate records
    isDuplicateFree = True
    unique = []
    for data in rsu_data:
        if data not in unique:
            unique.append(data)
    if len(unique) != len(rsu_data):
        isDuplicateFree = False
        return isDuplicateFree

    #check: empty file or empty records based on timeReceived key
    isEmpty = True
    for data in rsu_data:
        if bool(data) is False or (len(data["timeReceived"]) == 0):
            isEmpty = False
            break

    # have any checks failed?
    if (isDuplicateFree == False) or (isEmpty == False):
        isJSONclean = False

    return isJSONclean

def rsu_raw_bucket(client, filename, filepath, bucket_name):
    """
    Executes the transfer of raw data from the roadside unit to the 
    rsu_raw-ingest bucket in the GCP which stores raw, unclean data.

    Args:
        client: object referencing GCP Storage/Bucket Client
        filename: the name of raw RSU file passed as JSON object
        filepath: the location of the raw RSU file
        bucket_name: the name of the raw ingest bucket in the GCS
    """
    print("Beginning of bucket #1.")
    raw_bucket = client.get_bucket(bucket_name)
    raw_blob = raw_bucket.blob(filename)
    raw_blob.upload_from_filename(filename=filepath)
    
    # logging raw ingest upload message
    current_time = datetime.datetime.utcnow()                   
    log_message = Template('Raw ingest updated with new file at $time')
    logging.info(log_message.safe_substitute(time=current_time))
    
    print("End of bucket #1.")

def verify_and_copy_blobs_to_data_lake(list_blobs, raw_bucket, lake_bucket):
    """
    Helper function for the rsu_data_lake_bucket() function which
    publishes data as a byte string to the Pub/Sub topic.

    Args:
        list_blobs: the data to be stored in Pub/Sub
        raw_bucket: the GCS bucket holding raw ingest
        lake_bucket: the GCS bucket holding "clean" data
    """

    for blob in list_blobs:                                     # copying each RSU raw data file to the data lake
        data_string = blob.download_as_bytes()                  # data pulled as a BYTE string
        json_data = ndjson.loads(data_string)
        if is_json_clean(json_data) is True:                    # IF DATA IS CLEAN: copy the blob to the data lake
            raw_bucket.copy_blob(blob, lake_bucket)

def rsu_data_lake_bucket(client, r_bucket, l_bucket):
    """
    Executes the transfer of raw data from the rsu_raw-ingest bucket
    to the data lake bucket in the GCP to be cleaned/filtered/aggregated/etc.

    Args: 
        client: object referencing GCP Storage/Bucket Client
        raw_bucket: the GCS bucket holding raw ingest
        lake_bucket: the GCS bucket holding "clean" data
    """
    
    print("Beginning of bucket #2.")
    
    raw_bucket = client.get_bucket(r_bucket)            # source bucket
    lake_bucket = client.get_bucket(l_bucket)           # destination bucket
    raw_blobs = client.list_blobs(raw_bucket)
    verify_and_copy_blobs_to_data_lake(raw_blobs, raw_bucket, lake_bucket)
    
    # logging data push to the lake
    current_time = datetime.datetime.utcnow()    
    log_message = Template('Pushed data to the lake at $time')
    logging.info(log_message.safe_substitute(time=current_time))
    
    print("End of bucket #2.") 

def download_and_publish_blobs_to_data_warehouse(list_blobs, client, topic):
    """
    Helper function for the rsu_data_warehouse_bucket() function which
    publishes data as a byte string to the Pub/Sub topic.

    Args:
        client: object referencing GCP Pub/Sub Client
        list_blobs: the data to be stored in Pub/Sub
        topic: the Pub/Sub topic designated as the data warehouse
    """

    for blob in list_blobs:
        data_string = blob.download_as_bytes()                 # data MUST be a byte string
        future = client.publish(topic,data_string)              # when message is published, the client returns a "future"
        print(future.result())       

def rsu_data_warehouse_bucket(pub_client, storage_client, topic, bucket):
    """
    Will push data from the data lake to the designated Pub/Sub topic which
    will serve as a form of short-term data warehouse.

    Args:
        pub_client: object referencing GCP Publisher Client
        storage_client: object referencing GCP Storage/Bucket Client
        topic: the name of the data warehouse Pub/Sub topic name
        bucket: the name of the data lake GCS bucket
    
    """

    print("\nBeginning of bucket #3.")
    lake_bucket = storage_client.get_bucket(bucket)
    lake_blobs = storage_client.list_blobs(lake_bucket)          # retrieving data lake bucket
    download_and_publish_blobs_to_data_warehouse(lake_blobs, pub_client, topic)

    # logging publication message
    current_time = datetime.datetime.utcnow()    
    log_message = Template('Published message to the warehouse pub/sub topic at $time')
    logging.info(log_message.safe_substitute(time=current_time))

    print("End of bucket #3.")

def main(data, context):
    """
    Main function.
    Triggered from a message on a Cloud Pub/Sub topic.

    Args:
        data: (dict) Event payload.
        context: (google.cloud.functions.Context) Event metadata.
    """

    # setting the Google Application Credentials to JSON with service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\divav\Desktop\CDOT\gcp_test\CDOT CV ODE Dev-4d9416c81201.json"
    print("\nLoaded Google App credentials.")

    json_file = 'RSU-ND-clean.json'

    raw_ingest_bucket = 'rsu_raw-ingest'
    data_lake_bucket = 'rsu_data-lake'

    current_time = datetime.datetime.utcnow()
    log_message = Template('Cloud Function was triggered on $time')
    logging.info(log_message.safe_substitute(time=current_time))

    try:
        print("Begin filling buckets . . .")
        rsu_raw_bucket(Client(), "clean", json_file, 'rsu_raw-ingest')
        rsu_data_lake_bucket(Client(), raw_ingest_bucket, data_lake_bucket)
        topic_path = PublisherClient().topic_path('cdot-cv-ode-dev','rsu_data_warehouse')
        rsu_data_warehouse_bucket(PublisherClient(), Client(), topic_path, data_lake_bucket)
        
    except Exception as error:
        log_message = Template('Data transfer failed due to $message.')
        logging.error(log_message.safe_substitute(message=error))

if __name__ == '__main__':
    main('data', 'context')
