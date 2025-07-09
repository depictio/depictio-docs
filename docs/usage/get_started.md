# Getting Started with Depictio

This guide will help you get started with Depictio after installation. It covers the basic concepts and workflows to help you begin visualizing your data.

## First Steps

### Installation

If you haven't installed Depictio yet, please refer to the [installation guide](../installation/README.md) for detailed instructions on how to set up Depictio using Docker Compose, or Helm.

### Accessing the Web Interface

After installation [see the installation guide](../installation/README.md), you can access the Depictio web interface. If you used Docker Compose or the helm chart with a local setup, the default port is `5080`. Open your web browser and navigate to:

```bash
http://localhost:5080
```

### Logging In

When you first access Depictio, you'll be prompted to log in. The default installation creates an admin user with:

- **Email**: `admin@example.com`
- **Password**: `changeme`

<!-- markdownlint-disable MD046 -->
!!! warning "**Important**"
    Change the default password after your first login for security reasons.
<!-- markdownlint-enable MD046 -->

### Use depictio-cli

#### Install the CLI tool

Depictio provides a command-line interface (CLI) tool for managing data ingestion and other tasks. You can install the CLI tool by following the instructions in the [depictio-cli documentation](../installation/cli.md).

#### Create a CLI configuration

Once you have installed the CLI tool, you need to create a configuration file to interact with Depictio. This configuration file contains the necessary information to connect to your Depictio instance, including the base URL and user credentials.
To do so, go to the **profile** section in the web interface (bottom left corner).

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/profile_section.png" target="_blank">
        <img src="../../images/guides/get_started/profile_section.png" width="600">
    </a>
</div>

Once in the profile section, click in the **CLI Agents** button.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/cli_agents_button.png" target="_blank">
        <img src="../../images/guides/get_started/cli_agents_button.png" width="600">
    </a>
</div>

 You will land on the **CLI Agents** page, where you can manage your CLI configurations. To create a new configuration, click on the **Add new configuration** button.

 <div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/add_new_config.png" target="_blank">
        <img src="../../images/guides/get_started/add_new_config.png" width="600">
    </a>
</div>

 Select a name for your configuration and click on the **Save** button.

  <div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/config_save.png" target="_blank">
        <img src="../../images/guides/get_started/config_save.png" width="600">
    </a>
</div>

 This will generate a YAML file with the necessary configuration to interact with Depictio via the CLI. Save this file in a secure location (e.g., `~/.depictio/CLI.yaml`), and ensure it is not publicly accessible. Depending of your installation, the file will look like this:

```yaml
# ~/.depictio/CLI.yaml
base_url: http://localhost:8058
s3:
  bucket: depictio-bucket
  external_host: localhost
  external_port: 9000
  external_protocol: http
  external_service: false
  public_url: null
  root_password: minio123
  root_user: minio
  service_name: minio
  service_port: 9000
user:
  description: null
  email: admin@example.com
  flexible_metadata: null
  hash: null
  id: 6845c5892bf43fee63e14bab
  is_admin: true
  token:
    access_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
    created_at: '2025-06-08 19:34:21'
    description: null
    expire_datetime: '2026-06-08 19:34:21'
    flexible_metadata: null
    hash: null
    id: 6845e5bdce243952fac3e444
    logged_in: false
    name: TEST2
    token_lifetime: long-lived
    token_type: bearer
    user_id: 6845c5892bf43fee63e14bab
```

#### Use the CLI tool

You can now use the CLI tool to interact with your Depictio instance. For example, you can list available workflows, upload data collections, and manage your projects. Refer to the [depictio-cli documentation](../depictio-cli/usage.md) for detailed usage instructions.

In that get started guide, you can use the **palmer penguins dataset** to test the CLI tool. This dataset mimics the [palmer penguins dataset](https://allisonhorst.github.io/palmerpenguins/), which is a popular dataset for testing data visualization tools.

```bash
depictio-cli run \
    --CLI-config-path ~/.depictio/CLI.yaml \
    --project-config-path ../api/v1/configs/penguins_dataset/penguins_project.yaml
```

This command will run the CLI tool with the specified configuration file and project configuration file. This will create a new project in Depictio with the palmer penguins dataset, including 2 data collections: `physical_features` and `demographic_data`.

Once the data ingested into the system, you can go to the web interface and see the project created in the **Project Management** section.

### Creating Your First Dashboard

To create your first dashboard using the palmer penguins dataset, click on **+ New Dashboard** in the top right corner of the web interface.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/new_dashboard.png" target="_blank">
        <img src="../../images/guides/get_started/new_dashboard.png" width="600">
    </a>
</div>

 This will open the dashboard creation wizard. Select the **Palmer Penguins Species Comparison** project from the dropdown menu, and then click on **Create Dashboard**.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/new_dashboard_project_selection.png" target="_blank">
        <img src="../../images/guides/get_started/new_dashboard_project_selection.png" width="600">
    </a>
</div>

You will see a new dashboard created using the **Palmer Penguins Species Comparison** project.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../images/guides/get_started/new_dashboard_final.png" target="_blank">
        <img src="../../images/guides/get_started/new_dashboard_final.png" width="600">
    </a>
</div>

 Then follow the [dashboard creation guide](guides/dashboard_creation.md) and [dashboard usage guide](guides/dashboard_usage.md). These guides will walk you through the process of designing a dashboard, adding components, and configuring interactivity.

## Next Steps

Now that you understand the basics, you can:

- [Learn more about dashboard creation](guides/dashboard_creation.md)
- [Explore the dashboard components](guides/dashboard_usage.md)
- [Set up the CLI for your own data](../depictio-cli/usage.md)
- [Understand the API for integration](../api/overview.md)

## Troubleshooting

If you encounter issues:

- Check the [FAQ](../FAQ/general.md) for common problems and solutions
- Review the logs for error messages
- Ensure your data is in a supported format
- Verify that all services are running correctly
