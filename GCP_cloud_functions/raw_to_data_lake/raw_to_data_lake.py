from google.cloud import storage
import os
import json
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

def raw_to_data_lake(raw_bucket, lake_bucket,blob):
    """Triggered by new upload to the raw ingest storage bucket.
    Function retrieves this new upload and checks for cleanliness
    before sending clean data to the data lake bucket.
    Args:
         r_bucket: Raw ingest GCS bucket
         l_bucket: Data lake GCS bucket
         blob: Newest blob sent to raw ingest
    """
    
    # logging cloud function trigger
    current_time = datetime.datetime.now()
    log_message = Template('Cloud Function "raw-to-data-lake" was triggered at $time')
    logging.info(log_message.safe_substitute(time=current_time))
        
    try:
        data_string = blob.download_as_bytes()
        json_data = json.loads(data_string)
        if is_json_clean(json_data):
            raw_bucket.copy_blob(blob, lake_bucket)
            current_time = datetime.datetime.now()
            log_message = Template('Data lake updated at $time')
            logging.info(log_message.safe_substitute(time=current_time))

    except Exception as error:
        log_message = Template('Failed to perform operations on raw and/or data lake storage buckets due to $message')
        logging.error(log_message.safe_substitute(message=error))

def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    client = storage.Client()
    r_bucket = client.get_bucket(os.environ['raw_ingest_id'])
    l_bucket = client.get_bucket(os.environ['data_lake_id'])
    raw_blob = r_bucket.get_blob(event['name'])
    raw_to_data_lake(r_bucket,l_bucket,raw_blob)
  

