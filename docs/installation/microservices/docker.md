
# Docker Compose


Clone the repo:

```
git clone https://github.com/weber8thomas/depictio.git
```

Or if you want to use the jbrowse submodule:

```
git clone --recurse-submodules https://github.com/weber8thomas/depictio.git
```

If needed, example data can be downloaded by cloning the following repo:

```
git clone https://github.com/weber8thomas/depictio-data.git
```


Modify the `.env` file to update the environment variables. The following variables are mandatory to be set:


```
DEPICTIO_BACKEND_DATA_VOLUME_HOST=<path_to_your_data_folder>
```


Start the docker-compose services:

```
docker compose up -d --build
```