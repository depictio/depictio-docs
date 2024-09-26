
# Docker-compose setup

## Clone the repository

Clone the repo as well as its submodules:

```
git clone --recurse-submodules https://github.com/depictio/depictio.git
```

## Edit the configuration and create volumes

Edit the `.env` file to update the data volume path where your data is stored:


```
DEPICTIO_BACKEND_DATA_VOLUME_HOST=/ABSOLUTE/PATH/TO/depictio-data
```

Create volumes that will be used by the services:

```
mkdir -p depictio-data/ && chmod -R 777 depictio-data/
mkdir -p depictioDB/ && chmod -R 777 depictioDB/
mkdir -p minio_data/ && chmod -R 775 minio_data/
mkdir -p depictio/keys/ && chmod -R 775 depictio/keys/
mkdir -p depictio/.depictio/ && chmod -R 775 depictio/.depictio/
```

## Start the services

Start the docker-compose services (latest version accessible [here](https://github.com/depictio/depictio/blob/main/docker-compose.yaml)):

```
docker compose up -d --build
```

This will build the images and start the services. 



## List of services and corresponding URLs

The services will be available at the following URLs (with default ports and configurations):

* **Depictio frontend**: [http://localhost:5080](**http**://localhost:5080)
* **Depictio backend**: [http://localhost:8058](http://localhost:8058)
* **MinIO**: [http://localhost:9000](http://localhost:9000)
* **MinIO WebUI**: [http://localhost:9001](http://localhost:9001)
* **MongoDB**: [http://localhost:27018](http://localhost:27018)


