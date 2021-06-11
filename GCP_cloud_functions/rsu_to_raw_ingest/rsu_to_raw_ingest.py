from GCP_cloud_functions import config
from google.cloud import storage
import datetime
import logging
from string import Template

def rsu_to_raw_ingest(event, context):
    """Triggered by a Pub/Sub message published by the Cloud Scheduler.
    When a new message is published by the Scheduler, this function will
    pull from the RSU and send it to the raw ingest storage bucket. 
    For now, the RSU pull is simulated by the sample 'RSU-ND-clean.json' file.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    client = storage.Client()

    # logging cloud function trigger
    current_time = datetime.datetime.now()
    log_message = Template('Cloud Function "rsu-to-raw ingest" was triggered at $time')
    logging.info(log_message.safe_substitute(time=current_time))

    try:
        # retrieving raw ingest bucket and creating blob titled w/ timestamp of blob creation
        raw_bucket = client.get_bucket(config.config_vars['raw_ingest_id'])
        raw_blob = raw_bucket.blob(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        raw_blob.upload_from_filename(filename='RSU-ND-clean.json')

        # logging raw ingest upload
        current_time = datetime.datetime.now()
        log_message = Template('Raw ingest uploaded with new data at $time')
        logging.info(log_message.safe_substitute(time=current_time))

    except Exception as error:
        log_message = Template('Failed to perform operations on raw ingest storage bucket due to $message.')
        logging.error(log_message.safe_substitute(message=error))
            

