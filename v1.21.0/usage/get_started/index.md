# Getting Started with Depictio

This guide will help you get started with Depictio after installation. It covers the basic concepts and workflows to help you begin visualizing your data.

## First Steps

### Installation

If you haven't installed Depictio yet, please refer to the [installation guide](https://depictio.github.io/depictio-docs/latest/installation/index.md) for detailed instructions on how to set up Depictio using Docker Compose, or Helm.

### Accessing the Web Interface

After installation [see the installation guide](https://depictio.github.io/depictio-docs/latest/installation/index.md), you can access the Depictio web interface. If you used Docker Compose or the helm chart with a local setup, the default port is `5080`. Open your web browser and navigate to:

```
http://localhost:5080
```

### Logging In

When you first access Depictio, you'll be prompted to log in with the admin credentials you set before starting the service.

Admin credentials are set at installation time

The initial admin account is created from two environment variables that must be configured **before the first start**:

- `DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` — the admin email address
- `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD` — the admin password (≥ 16 characters; the server refuses to start if this is absent or too short)

See the [installation configuration guide](https://depictio.github.io/depictio-docs/latest/installation/configuration/index.md) for details on where and how to set these variables.

### Use existing demo data

If you want to explore Depictio with existing demo data, you can use the provided registered iris dataset. A demo dashboard is also already created for you to explore. You can access it by clicking on the **"Iris Dashboard"** on the landing page.

### Register your first project

#### Using the Web Interface

1. **Open Projects**: click **Projects** in the sidebar, then **New project**.
1. **Describe the project**: enter a **Project name** and, optionally, a **Description**. Tick **Make this project public** to let every user see it.
1. **Click Add data**: this opens three steps, **Your data**, **What Depictio found** and **Create**. **Create without data** makes an empty project instead.
1. **Your data**: drop files or folders on **Upload** (CSV, TSV, Parquet, Feather and more, 50 MB each). Or use **Read in place** for a folder, a bucket or one file URL, read where it is.
1. **Check how it is read**: for a folder, **How should Depictio read this folder?** preselects **Flat tables**, **Custom workflows** or **Pipeline template**. A recognised pipeline shows as **Pipeline:** *name* **· Detected**, with **Change** to pick another.
1. **What Depictio found**: check the tables, runs and source Depictio lists. Then click **Create project with N tables**, or **Next** and **Create Project** for a pipeline.

[![](../../images/guides/project-creation/create-project-from-folder.webp)](../../images/guides/project-creation/create-project-from-folder.mp4)

See [Create a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#create-a-project) for every option, and [Add data](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#add-data) to add tables or runs later.

#### Using the CLI

Use the command-line interface to programmatically manage your Depictio projects and data.

##### Install the CLI

Depictio provides a command-line interface (CLI), the `depictio` command, for managing data ingestion and other tasks. You can install it by following the [CLI installation guide](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md).

##### Create a CLI configuration

Once you have installed the CLI tool, you need a configuration file to interact with Depictio. It holds the address of your Depictio instance and a long-lived token that signs the CLI in as you.

1. Open **Account settings** with your avatar in the top bar, and the **CLI agents** section (v1.17.0+; before, a separate CLI agents page).

1. Click **Add configuration**, give the configuration a name that tells it apart, such as the machine it runs on, and click **Create**.

1. **Save it**: **Download** the file, or **Copy** it, as `~/.depictio/CLI.yaml`. The token is shown only once, and it signs the CLI in as you: keep the file private.

1. **Check the connection** from the machine you saved it on:

   ```
   depictio config check
   ```

The file looks like this (abridged):

```
# ~/.depictio/CLI.yaml
api_base_url: http://localhost:8058
user:
  id: 67658ba033c8b59ad489d7c7
  email: admin@example.com
  is_admin: true
  token:
    access_token: >-
      eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
    token_type: bearer
    token_lifetime: long-lived
    expire_datetime: '2027-10-12 13:59:59'
    name: laptop
s3_storage:
  service_name: localhost
  service_port: 9000
  external_host: localhost
  external_port: 9000
  external_protocol: http
  bucket: depictio-bucket
  root_user: minio
  root_password: minio123
```

##### Use the CLI tool

You can now use the CLI tool to interact with your Depictio instance. For example, you can list available workflows, upload data collections, and manage your projects. Refer to the [CLI usage documentation](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md) for detailed usage instructions.

Saved as `~/.depictio/CLI.yaml`, the configuration is the one every command uses by default, so none of them needs `--server`. See [Which server a command uses](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#choosing-a-server) for the other ways to name a server.

With no `~/.depictio/CLI.yaml`, the CLI uses the [local server](https://depictio.github.io/depictio-docs/latest/installation/local/index.md): here pipeline results are previewed, then ingested into it:

In that get started guide, you can use the **palmer penguins dataset** to test the CLI tool. This dataset mimics the [palmer penguins dataset](https://allisonhorst.github.io/palmerpenguins/), which is a popular dataset for testing data visualization tools.

```
depictio ingest \
    --project-config-path ../api/v1/configs/penguins_dataset/penguins_project.yaml
```

This command will run the CLI tool with the default configuration file and the specified project configuration file. This will create a new project in Depictio with the palmer penguins dataset, including 2 data collections: `physical_features` and `demographic_data`.

Once the data is ingested, the project appears on the **Projects** page. On the project page, **Project settings** holds its **Storage**, **Data refresh**, **Export** and **Create a template** sections, plus **Send** where migration is on.

##### Video Tutorial

[![](../../images/guides/web-ui/cli-config.webp)](../../images/guides/web-ui/cli-config.mp4)

#### Creating Your First Dashboard

To create your first dashboard using the palmer penguins dataset, click on **+ New Dashboard** in the top right corner of the web interface.

This will open the dashboard creation modal. Pick the **Palmer Penguins Species Comparison** project, give the dashboard a name, and confirm.

You will land in the editor for the new dashboard, where you can add components. The screenshot below shows the editor against an existing ampliseq dashboard for reference.

Then follow the [dashboard creation guide](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md) and [dashboard usage guide](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_usage/index.md). These guides will walk you through the process of designing a dashboard, adding components, and configuring interactivity.

## Next Steps

Now that you understand the basics, you can:

- [Learn more about dashboard creation](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md)
- [Explore the dashboard components](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_usage/index.md)
- [Set up the CLI for your own data](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md)
- [Understand the API for integration](https://depictio.github.io/depictio-docs/latest/api/overview/index.md)

## Troubleshooting

If you encounter issues:

- Check the [FAQ](https://depictio.github.io/depictio-docs/latest/FAQ/general/index.md) for common problems and solutions
- Review the logs for error messages
- Ensure your data is in a supported format
- Verify that all services are running correctly
- [Report an issue on GitHub](https://github.com/depictio/depictio/issues) for bugs or feature requests
