from GCP_cloud_functions.raw_to_data_lake import raw_to_data_lake
from google.api_core import exceptions
from google.cloud import exceptions
import mock
import os
import pytest
import unittest

# Here we can test with the existing methods


@mock.patch.object(raw_to_data_lake, "raw_to_data_lake")
@mock.patch("google.cloud.storage.Client", autospec=True)
def test_main_ExceptionRaised_BucketNotFound(mockClient, mockRawToDataLakeFunction):
    # Arrange
    os.environ['raw_ingest_id'] = 'raw_id'
    os.environ['data_lake_id'] = 'data_lake_id'
    event = None
    context = None
    mockClient().get_bucket.side_effect = exceptions.NotFound('testing')

    # Act
    with pytest.raises(exceptions.NotFound):
        raw_to_data_lake.main(event, context)

    # Assert
    assert not mockRawToDataLakeFunction.called


#############################################
# Here we add a testing class and pass in unittest.TestCase
# along with 'self' to the test method. we can then assert that exceptions are raised
class TestRawToDataLake(unittest.TestCase):

    @mock.patch.object(raw_to_data_lake, "is_json_clean", return_value=True)
    @mock.patch.object(raw_to_data_lake, "raw_to_data_lake")
    @mock.patch("google.cloud.storage.Client", autospec=True)
    def test_main_ExceptionRaised_BucketNotFound(self, mockClient, mockRawToDataLakeFunction, mockIsJsonCleanFunction):
        # Arrange
        os.environ['raw_ingest_id'] = 'raw_id'
        os.environ['data_lake_id'] = 'data_lake_id'
        event = None
        context = None
        mockClient().get_bucket.side_effect = exceptions.NotFound('testing')

        myTestVal = mockIsJsonCleanFunction("")

        # Act / Assert
        # unittest.TestCase.assertRaises
        with self.assertRaises(exceptions.NotFound) as notFoundError:
            raw_to_data_lake.main(event, context)

        # Assert
        assert not mockRawToDataLakeFunction.called
