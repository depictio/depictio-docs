# Getting started





## Ingest example data 

### depictio-cli setup

!!! note
    * The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register data collections and workflows, as well as to submit jobs. The depictio-cli is currently in development and is not yet ready for production use.
    * Prerequisite: virtualenv or conda needs to be installed on your machine.


To ingest example data, you can use the depictio-cli. The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register data collections and workflows, as well as to submit jobs. The depictio-cli is currently in development and is not yet ready for production use.


Clone the depictio-cli repository:

```bash
https://github.com/depictio/depictio-cli.git
```

Create the depictio-cli python venv using the following:

```bash
# Set up a virtual environment
python -m venv depictio-cli-venv

# Activate the virtual environment
source depictio-cli-venv/bin/activate 

# Install the depictio-cli package
pip install -e . 

# Add the depictio package to the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PWD/depictio-cli
```

### Running the ingestion command through the depictio-cli

Using the depictio-cli, you can ingest example data by running the following command:

```bash
depictio-cli data setup \
    --agent-config-path ../depictio/.depictio/default_admin_agent.yaml \
    --pipeline-config-path configs/mosaicatcher_pipeline/mosaicatcher_pipeline.yaml \
    --scan-files
```

The depictio-cli will do the following:

* Validate the agent configuration against the API to ensure that the token is valid and user has the necessary permissions.
* Validate the pipeline configuration against the API to ensure that the configuration is valid.
* Register the workflows and data collections with the API.
* Iterate through the files in the data directory listed in the pipeline configuration, create corresponding file objects in the mongo database, and associate them with the data collections.

Then the depictio-backend will iterate through the files in the data directory listed in the pipeline configuration, and accordingly to the data collections created:

* Data collection of type Table: Read each of the file, aggregate them into a DeltaLake format, and store them in the MinIO bucket.
* Data collection of type JBrowse: Transfer the files to the MinIO bucket in a specific files structure that is compatible with JBrowse and Depictio.


----

!!! danger "#TODO"

    * Show a log example of the result of the ingestion
    * Logging through the admin default credentials
    * Example dataset 