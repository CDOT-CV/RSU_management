# RSU Connected Vehicle Monitor

This is a proof-of-concept for the RSU Connected Vehicle monitor for the Colorado Department of Transportation.  This project is a web application that was written in Angular (Angular CLI v.12.0.1, Node v.14.17.0, and package manager npm v.6.14.13) and used the Mapbox package. 

This repository contains the necessary files needed to deploy the web app: the `app.yaml` file and the project files directory titled `poc-rsu-dashboard/`. The former file is the configuration file that will be used by the Google Cloud Platform (GCP) App Engine to deploy the project. The latter directory contains the project files for the web app itself. 

## Obtaining a Mapbox Token
In order to utilize the Mapbox package in Angular (used to display the map of Colorado and all relevant RSU markings and contains all map functions), a Mapbox token is required. Mapbox uses JSON Web Tokens (JWT) to associate API requests with an account. 

To obtain a Mapbox token: 
1. Create a Mapbox account (this should be free of charge).
2. Visit account.mapbox.com with your credentials, and click the 'Tokens' page.
3. Every account is given a free default public token - this will provide sufficient access to the needed tools for this Angular project. (A personalized token can also be created.)
4. The token is injected into the `poc-rsu-dashboard\src\environments\environment.ts`. Copy the value into the parameter.


## Building the Angular project
Before the web app can be deployed to the cloud, it must first be built. 
1. After downloading the project files to the local machine, navigate to the directory via terminal.
```
cd local_angular_app
```
2. Run the following command to build the Angular app for production (this makes use of the Angular CLI).
```
ng build --prod
```
This will create a `dist/` folder in the local project root directory. This `dist` folder contains the local_angular_app folder, and should basically contain the following files (may slightly vary).
```bash
 3rdpartylicenses.txt
 es2015-polyfills.1e04665e16f944715fd2.js
 favicon.ico
 index.html
 main.39049915a67858ea8ac0.js
 polyfills.8bbb231b43165d65d357.js
 runtime.26209474bfa8dc87a77c.js
 styles.3ff695c00d717f2d2a11.css
```
A pre-built `dist/` directory is included in the repository in the project files.

## Setting up the Google Cloud Platform (GCP) 

Assuming that a Google account and an active project is created, proceed with the following:

1. Create a bucket in the Google Cloud Storage.
2. Go to this bucket and select the "UPLOAD FILES" options to upload the `app.yaml` file and the "UPLOAD FOLDER" option to upload the `dist/` folder.
3. Open the Google Cloud Interactive Shell.
4. Once connected to the Cloud Shell, create a directory for the web app.
```
mkdir name_of_gcp_webapp_dir
```
5. Sync the data from the created bucket into the directory just created.
```
gsutil rsync -r gs://name-of-rsu-webapp-bucket ./name_of_gcp_webapp_dir
```
6. Navigate to the created cloud directory.
```
cd name_of_gcp_webapp_dir
```
7. Run the following command to deploy the app.
```
gcloud app deploy
```
Note: for first-time deployment, the project will need to be configured. Answer appropriately when prompted (for instance, enter "Y" when prompted "Do you want to continue (Y/n)?")
8. Once the deployment is completed, run the app to obtain the GCP-provided URL hosting the web app.
```
gcloud app browse
```
The link will be displayed. 

## Contributors
This project was created by CDOT-OIM intern Dhivahari Vivek. For questions about this project, however, please contact djohnston@neaeraconsulting.com.