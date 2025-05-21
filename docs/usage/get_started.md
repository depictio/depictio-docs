# Getting Started with Depictio

This guide will help you get started with Depictio after installation. It covers the basic concepts and workflows to help you begin visualizing your data.

## Overview

Depictio is a platform for creating interactive dashboards for bioinformatics data visualization. It consists of:

1. A **backend API** that manages data, users, and configurations
2. A **frontend** that provides the user interface for creating and viewing dashboards
3. A **CLI tool** for data ingestion and management

## First Steps

### Accessing the Web Interface

After installation [see the installation guide](../installation/README.md), you can access the Depictio web interface. If you used Docker Compose or the helm chart with a local setup, the default port is `5080`. Open your web browser and navigate to:

```bash
http://localhost:5080
```

### Logging In

When you first access Depictio, you'll be prompted to log in. The default installation creates an admin user with:

- **Email**: `admin@example.com`
- **Password**: `changeme`

!!! warning "**Important**"

<!-- markdownlint-disable MD046 -->

    Change the default password after your first login for security reasons.

<!-- markdownlint-enable MD046 -->

## Understanding the Interface

The Depictio interface is organized into several main sections:

### Dashboards management View

This is the landing page where you can view and manage your dashboards. Key features include:

- **Dashboard list**: View all your dashboards
- **Create new dashboard**: Start a new dashboard project
- **Edit existing dashboards**: Modify name, duplicate or delete existing dashboards
- **Share dashboards**: Make public or private dashboards at the instance level

### Dashboard design View

When clikking on a dashboard, you enter the design view. This is where you can create and edit your dashboards. Key features include:

- **Component library**: Available visualization components
- **Layout editor**: Drag-and-drop interface for arranging components
- **Property editor**: Configure component properties using data collections registered in the project
- **Interactivity settings**: Enable or disable interactivity between components
- **Save**: Auto-save feature and manual save option to trigger a screenshot for the dashboard thumbnail

### Project Management

This section allows you to manage your projects and data. Key features include:

- **Project list**: View and manage your projects
- **Workflow management**: List workflows registered in the project and their metadata
- **Data collections**: List each data collection of each workflow and their metadata. Preview the data collection in a table format.

## Basic Workflow

The typical workflow in Depictio consists of:

1. **Project Setup**: Create a YAML project configuration (workflows, data collections, and metadata). See refer
2. **Data Ingestion**: Import data using the CLI tool
3. **Dashboard Creation**: Design dashboards to visualize your data
4. **Sharing**: Share dashboards with collaborators

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
