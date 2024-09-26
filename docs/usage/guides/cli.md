
# Depictio CLI setup

!!! note
    * The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register data collections and workflows, as well as to submit jobs. The depictio-cli is currently in development and is not yet ready for production use.
    * Prerequisite: virtualenv or conda needs to be installed on your machine.


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

```bash
depictio-cli data setup \
    --agent-config-path ../depictio/.depictio/default_admin_agent.yaml \
    --pipeline-config-path configs/mosaicatcher_pipeline/mosaicatcher_pipeline.yaml \
    --scan-files
```


# Reference

::: src.test.MyClass
    handler: python
    options:
      members:
        - method_a
        - method_b
      show_root_heading: true
      show_source: true