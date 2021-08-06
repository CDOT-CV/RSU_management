import time
from google.cloud import bigquery
from datetime import datetime, timedelta

def query_rsu_counts(rsu_ip):
    client = bigquery.Client()
    
    tablename = "cdot-oim-cv-dev.RsuManagerDataset.rsucounts"
    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    query = "SELECT RSU, BsmCount " \
            f"FROM `{tablename}` " \
            f"WHERE RSU = \"{rsu_ip}\" " \
            f"AND Date = \"{yesterday}\""
    query_job = client.query(query)

    result = {"count": 0}
    for row in query_job:
        result["count"] = row["BsmCount"]

    return result


def entry(request):
  if request.method == 'OPTIONS':
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600'
    }

    return ('', 204, headers)
  
  headers = {
    'Access-Control-Allow-Origin': '*'
  }

  return (query_rsu_counts(request.args['rsuIp']), 200, headers)