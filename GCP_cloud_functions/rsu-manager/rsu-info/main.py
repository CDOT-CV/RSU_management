import os
import sqlalchemy

db_config = {
  # Pool size is the maximum number of permanent connections to keep.
  "pool_size": 5,
  # Temporarily exceeds the set pool_size if no connections are available.
  "max_overflow": 2,
  # Maximum number of seconds to wait when retrieving a
  # new connection from the pool. After the specified amount of time, an
  # exception will be thrown.
  "pool_timeout": 30,  # 30 seconds
  # 'pool_recycle' is the maximum number of seconds a connection can persist.
  # Connections that live longer than the specified amount of time will be
  # reestablished
  "pool_recycle": 60  # 1 minutes
}

db = None

def init_tcp_connection_engine():
  db_user = os.environ["DB_USER"]
  db_pass = os.environ["DB_PASS"]
  db_name = os.environ["DB_NAME"]
  db_host = os.environ["DB_HOST"]

  # Extract host and port from db_host
  host_args = db_host.split(":")
  db_hostname, db_port = host_args[0], int(host_args[1])

  print(f"Creating DB pool to {db_hostname}:{db_port}")
  pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(
      drivername="postgresql+pg8000",
      username=db_user,  # e.g. "my-database-user"
      password=db_pass,  # e.g. "my-database-password"
      host=db_hostname,  # e.g. "127.0.0.1"
      port=db_port,  # e.g. 5432
      database=db_name  # e.g. "my-database-name"
    ),
    **db_config
  )

  pool.dialect.description_encoding = None
  print("DB pool created!")
  return pool

def getRsuData():
  global db
  if db is None:
    db = init_tcp_connection_engine()

  result = {"rsuList": []}

  print("DB connection starting...")
  with db.connect() as conn:
    # Execute the query and fetch all results
    query = "SELECT jsonb_build_object('type', 'Feature', 'id', \"RsuDataId\", 'geometry', ST_AsGeoJSON(\"Geography\")::jsonb, 'properties', to_jsonb(row)) FROM (SELECT * FROM public.\"RsuData\") row"
    
    print(f'Executing query "{query};"...')
    data = conn.execute(query).fetchall()

    print('Parsing results...')
    i = 0
    for point in data:
      point = dict(point[0])
      if i == 20:
        point["onlineStatus"] = "offline"
        i = 0
      else:  
        point["onlineStatus"] = "online"
        i += 1
        
      result["rsuList"].append(point)

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

  return (getRsuData(), 200, headers)

#if __name__ == "__main__":
#  r = entry("test")
#  print(r)
