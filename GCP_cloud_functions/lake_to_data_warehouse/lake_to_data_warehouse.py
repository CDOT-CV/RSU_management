from google.cloud import storage 
from google.cloud import pubsub_v1
import datetime
import logging
import os
from string import Template

def rsu_data_warehouse_bucket(publisher, pubsub_topic, lake_blob):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         pubsub_topic: The pubsub topic serving as the short-term data hub.
         lake_blob: Most recent data pushed to the data lake GCS bucket.
    """

    # logging cloud function trigger
    current_time = datetime.datetime.now()
    log_message = Template('Cloud Function "lake-to-data-warehouse" was triggered at $time')
    logging.info(log_message.safe_substitute(time=current_time))
        
    try:
        data_string = lake_blob.download_as_bytes()
        future = publisher.publish(pubsub_topic,data_string)
        print(future.result())
            
        # logging publication message
        current_time = datetime.datetime.utcnow()    
        log_message = Template('Published message to the data hub pub/sub topic at $time')
        logging.info(log_message.safe_substitute(time=current_time))

    except Exception as error:
        log_message = Template('Failed to perform actions with data warehouse Pub/Sub topic due to $message')
        logging.error(log_message.safe_substitute(message=error))
    
def main(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pub_client = pubsub_v1.PublisherClient()
    client = storage.Client()

    topic = pub_client.topic_path(os.environ['project_id'], os.environ['data_hub_id'])
    blob = client.get_bucket(event['bucket']).get_blob(event['name'])
    rsu_data_warehouse_bucket(pub_client, topic, blob)
