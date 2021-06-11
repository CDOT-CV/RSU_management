
# RSU Data Manager

| Build       | Quality Gate     | Code Coverage     |
| :------------- | :----------: | -----------: |
|  [![Build Status](https://travis-ci.com/CDOT-CV/RSU_Management.svg?branch=dev)](https://travis-ci.com/CDOT-CV/RSU_Management) | [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=dev&project=CDOT-CV_RSU_Management&metric=alert_status)](https://sonarcloud.io/dashboard?id=CDOT-CV_RSU_Management&branch=dev)   | [![Coverage](https://sonarcloud.io/api/project_badges/measure?branch=dev&project=CDOT-CV_RSU_Management&metric=coverage)](https://sonarcloud.io/dashboard?id=CDOT-CV_RSU_Management)    |

## Project Description

This project is an open-source, proof-of-concept for the roadside unit (RSU) data manager with the integration of Google Cloud Storage (GCS) functions. RSU data is assumed to take the form of JSON strings. The data will be passed through three "containers". First, all data will be placed in the raw ingest (a GCS bucket). From there, each data is checked for cleanliness: if the check passes, the clean data is placed in the data lake (another GCS bucket). From there, data is pushed as byte string messages to the short-term data warehouse (a Google Cloud Pub/Sub topic).

The data_manager directory contains two sub-directories: sample_files and source_code. The former directory holds the sample_files used during the design, implementation and testing of this project. The RSU-ND.json file is an example of the type of JSON string retrieved from an RSU. The sample_creds.json file is an example format of the credentials issued by the Google Cloud Platform (GCP), which is passed into the main.py script and enables the user to access the GCP.

## Guidelines

- Issues
  - Create issues using the SMART goals outline (Specific, Measurable, Actionable, Realistic and Time-Aware).
- PR (Pull Requests)
  - Create all pull requests from the master branch. 
  - Create small, narrowly focused pull requests.
  - Maintain a clean commit history so that they are easier to review.

## Prerequisites and Set-Up

### Local Environment Set-Up

This project supports Python >= 3.5. Refer to the requirements.txt document to [pip](https://pip.pypa.io/en/stable/) install the necessary packages. The Google Cloud Storage Python packages, for example, would be installed using:

```bash
pip install google-cloud-bigquery
pip install google-cloud-storage
pip install google-cloud-pubsub
```

Alternatively, install all necessary packages using:

```bash
pip install -r .\requirements.txt
```

### Local Google Cloud Platform Set-Up

In order to properly leverage the GCP's features when running the script on a local machine, the user must verify that their GCP admin has granted the user's GCP Client both Storage and Pub/Sub Admin privileges. Additionally, it may be helpful to grant these privileges on a user account-basis.

If the user runs the script on a local machine, they must also retrieve the JSON credentials for the service account used from their GCP administrator. The path to this JSON file will be assigned to the "GOOGLE_APPLICATION_CREDENTIALS" environment variable, as shown in the def main() function of the data_manager/source_code/main.py script.

If the user refactors the script to leverage Google Cloud Functions, including these credentials in the script itself are likely not necessary.

## How to Run

The integration of RSUs into this script is yet to come. At present, the script (main.py) uses the RSU sample file 'RSU-ND-clean.json' (found in the data_manager/sample_files and referenced in the def main() function of the main.py script). This sample file accompanies the main.py script in data_manager/source_code. When running locally, ensure that main.py and the sample script are located in the same folder.
 
To run this code on a local machine:

```
python3 main.py
```

## Google Cloud Storage (GCS): Cloud Function Set-Up

The modularized code in main.py can be easily refactored into smaller modules, or Cloud Functions, in the GCP. CDOT's implementation divided main.py into three Cloud Functions, and the GCP_cloud_functions directory contains the files necessary for each GCP Cloud Function set-up. For instance, the GCP_cloud_functions/rsu-to-raw-ingest folder contains every file needed to set up and deploy the rsu-to-raw-ingest Cloud Function (which will pull new data from the RSU and send it to the data bucket containing the raw ingest). Additionally, the config.py file contains the storage/container identifiers used in each Cloud Function, and must be included in each individual Cloud Function deployment.

CDOT's Cloud Function set-up refactors main.py into three Cloud Functions: 

- **rsu-to-raw-ingest** function: retrieves the raw data ingest from the RSU(s) and sends it to the designated data bucket in the GCS which stores the raw ingest. This function is triggered by a Pub/Sub topic receiving timely messages from the Cloud Scheduler. For instance, the Cloud Scheduler may publish a message to this Pub/Sub topic every five minutes, triggering the Cloud Function to pull from the RSU and send to the designated data bucket every five minutes.
- **raw-to-data-lake** function: retrives new uploads from the data ingest bucket and "checks" its cleanliness before sending approved, "clean" data to the designated "data lake" storage bucket in the GCS. At present, the function checks for duplicate timestamps and for records with missing values. If a record is found to have records with duplicate timestamps and/or missing values, that file will not be pushed to the data lake and will remain in the raw ingest. As this proof-of-concept expands, the function will likely include more checks. This function is triggered by any new data upload to the data ingest storage bucket.
- **lake-to-data-warehouse** function: retrives new uploads from the data lake bucket and publishes this data to a short-term "data warehouse" Pub/Sub thread as a byte string. This function is triggered by any new data upload to the data lake storage bucket. 

### Diagram of Preliminary Cloud Function Set-Up in the GCS

The following diagram details the current GCS set-up of the Cloud Functions (including triggers), the required storage buckets and Pub/Sub topics, and the scheduler. 

![Diagram of GCP Cloud Function Set Up](GCP_cloud_functions/GCPfunction_setup.png?raw=true)

## Testing

### Prerequisites and Set-Up

The following packages must be pip installed in order to run test_main.py (the unit tests):

```bash
pip install mock
pip install unittest
pip install pytest
pip install google-cloud-storage
pip install google-cloud-pubsub
```

The test for the main.py script is the test_main.py script, which can be found in the /tests directory. 

### How to Run

To run the test script on a local machine:

```
python -m pytest test_main.py
```

## Contributors
For any questions, contact Dhivahari Vivek at dhivahari.vivekanandasarma@state.co.us.
