from GCP_cloud_functions.lake_to_data_warehouse import lake_to_data_warehouse
import mock
import os

@mock.patch("google.cloud.pubsub_v1.PublisherClient")
@mock.patch("google.cloud.storage.Client")
def test_lake_to_data_warehouse_success(client, publish_client):

    topic = publish_client().topic_path('project_id', 'data_hub_id')
    l_bucket = client().get_bucket('test_data_lake_bucket')
    lake_blob = l_bucket.blob('test')
    lake_blob.upload_from_string('{"timeReceived": "2020-05-14T11:37:06Z", "year": "2020", "month": "05", "day": "14", "hour": "11", "version": "1.1.0", "type": "bsm"}')

    lake_to_data_warehouse.rsu_data_warehouse_bucket(publish_client(), topic, lake_blob)
    publish_client().publish.assert_called_with(topic, client().get_bucket().blob().download_as_bytes())

@mock.patch.object(lake_to_data_warehouse, "rsu_data_warehouse_bucket")
@mock.patch("google.cloud.storage.Client")
def test_main_NotCalled_BlobNotFound(mockClient, mockLakeToDataWarehouseFunction):
    
    event = {
        'bucket': 'rsu_data-lake',
        'name': 'test',
        'metageneration': 'some-metageneration',
        'timeCreated': '0',
        'updated': '0'
    }
    context = None
    l_bucket = mockClient().get_bucket(event['bucket'])
    l_bucket.get_blob.side_effect = None    # get_blob returns None if blob does not exist

    assert not mockLakeToDataWarehouseFunction.called

@mock.patch.object(lake_to_data_warehouse, "rsu_data_warehouse_bucket")
@mock.patch("google.cloud.pubsub_v1.PublisherClient")
@mock.patch("google.cloud.storage.Client")
def test_main_NotCalled_TopicNotFound(mockClient, mockPublisher, mockLakeToDataWarehouseFunction):

    os.environ['project_id'] = 'project_id'
    os.environ['data_hub_id'] = 'hub_id'

    event = None
    context = None

    topic = mockPublisher.topic_path(os.environ['project_id'], os.environ['data_hub_id'])
    mockPublisher.topic_path.side_effect = None

    assert not mockLakeToDataWarehouseFunction.called

@mock.patch.object(lake_to_data_warehouse, "rsu_data_warehouse_bucket")
@mock.patch("google.cloud.pubsub_v1.PublisherClient")
@mock.patch("google.cloud.storage.Client")
def test_main_Success(mockClient, mockPublisher, mockLakeToDataWarehouseFunction):
    event = mock.MagicMock()
    context = mock.MagicMock()    
    os.environ['project_id'] = 'project_id'
    os.environ['data_hub_id'] = 'hub_id'
    lake_to_data_warehouse.main(event, context)

    mockPublisher().topic_path.assert_called_with(os.environ['project_id'], os.environ['data_hub_id'])
    mockClient().get_bucket.assert_called_with(event['bucket'])
    mockClient().get_bucket(event['bucket']).get_blob.assert_called_with(event['name'])
    assert mockLakeToDataWarehouseFunction.called
    
    
