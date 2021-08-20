# RSU Manager Cloud Functions
The RSU Manager is a web application that uses multiple cloud functions as a backend that pulls data together and returns it to the web application in the desired format. These cloud functions are deployed in GCP Cloud Functions and are triggered over HTTP.  However, these cloud functions are not directly triggered from the web application. The web application directly makes requests from a GCP API Gateway via defined endpoints which then redirect the traffic to their designated cloud function.

## API Gateway
The API gateway is created using the following YAML, [rsu-manager-api-config.yaml](rsu-manager-api-config.yaml). To create an API Gateway the following commands must be run:

- `gcloud api-gateway apis create rsu-manager-api --project=project-name`
- `gcloud api-gateway api-configs create rsu-manager-api-config --api=rsu-manager-api --openapi-spec=rsu-manager-api-config.yaml --project=project-name`
- `gcloud api-gateway gateways create rsu-manager-apigateway --api=rsu-manager-api --api-config=rsu-manager-api-config --location=us-central1 --project=project-name`

The GCP API Gateway uses Swagger/OpenAPI YAML to customize the endpoints of the REST service. This gateway assumes you have created and deployed the GCP cloud functions.

## Cloud Function: RSU Info
This cloud function allows the RSU Manager web application to receive all basic data for RSUs in the GCP Cloud SQL database. It performs a basic select all query from a table named "RsuData" that is located in a database specified by the environments variables.

<b>Environment Variables:</b>
- DB_USER: The database user that will be used to authenticate the cloud function when it queries the database.
- DB_PASS: The database user's password that will be used to authenticate the cloud function.
- DB_NAME: The database name.
- DB_HOST: The database's hostname or IP.

It is important to note that this cloud function will need to be deployed with a VPC link to the VPC that the Cloud SQL database is also located on so it is able to route directly to the database. A publicly accessible endpoint for the database cannot white list the cloud function due to GCP Cloud Functions not having a guaranteed static endpoint. This can be averted with the use of a VPC Link.

## Cloud Function: RSU Query Counts
This cloud function allows the RSU Manager web application to receive the message counts for a single, selected RSU from a BigQuery table. It performs a basic select query on a table specified by the environments variable.

<b>Environment Variables:</b>
- COUNT_DB_NAME: The BigQuery table name where the RSU message counts are located.