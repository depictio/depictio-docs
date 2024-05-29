
## Current setup

Clone the repo:

```
git clone https://github.com/weber8thomas/depictio.git
```

Or if you want to use the jbrowse submodule (which is not mandatory) use the following command to clone the repo with the submodule:

```
git clone --recurse-submodules https://github.com/weber8thomas/depictio.git
```

If needed, example data can be downloaded by cloning the following repo:

```
git clone https://github.com/weber8thomas/depictio-data.git
```




Create and modify the `.env` file to update the environment variables. The following variables are mandatory to be set:


```
DEPICTIO_BACKEND_DATA_VOLUME_HOST=/ABSOLUTE/PATH/TO/depictio-data
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
AUTH_PRIVATE_KEY=<your_public_key>
AUTH_PUBLIC_KEY=<your_secret_key>
```

Create the MongoDB data folder and assign the correct permissions:

```
mkdir -p depictioDB/ && chmod 777 depictioDB/
```


Start the docker-compose services:

```
docker compose -f docker-compose.yml up -d
```

The services will be available at the following URLs (with default ports and configurations):

* **Depictio frontend**: [http://localhost:5080](http://localhost:5080)
* **Depictio backend**: [http://localhost:8058](http://localhost:8058)
* **MinIO**: [http://localhost:9000](http://localhost:9000)
* **MinIO WebUI**: [http://localhost:9001](http://localhost:9001)
* **MongoDB**: [http://localhost:27018](http://localhost:27018)

Create the depictio-cli python venv using the following:

```bash
# Set up a virtual environment
python -m venv depictio-cli-venv

# Activate the virtual environment
source depictio-cli-venv/bin/activate

# Install dependencies from requirements file
pip install -r requirements/depictio-cli-requirements.txt

# Add the depictio package to the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PWD/depictio
```

Then, create a default user (Paul Cezanne) in the mongoDB with the following command:

```bash
python depictio/api/v1/configs/create_user_mongodb.py
```

And create a user token with the following command:

```bash
python depictio-cli/depictio_cli/depictio_cli.py create-user-and-return-token
```

This will create a default user (Paul Cezanne) as well as a configuration in your home folder: `~/.depictio-cli/config.yaml`. This file contains the user token and the backend URL.

```yaml
DEPICTIO_API: http://localhost:8058
email: paul.cezanne@embl.de
token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
user:
  email: paul.cezanne@embl.de
  password: paul
  username: cezanne
```

Update the `.env` file with the following variables:

```
AUTH_TMP_TOKEN=<token_defined_in_the_config.yaml>
```

Restart the docker-compose services with the following command in order to update the environment variables:

```
docker compose -f docker-compose.yml up -d --force-recreate
```

You can now register data collections and workflows using the depictio-cli using:
    
```bash
python depictio-cli/depictio_cli/depictio_cli.py setup \
    --config_path configs/mosaicatcher_pipeline/mosaicatcher_pipeline.yaml \
    --scan_files
```