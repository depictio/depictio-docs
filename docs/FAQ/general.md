# Frequently Asked Questions

This page addresses common questions about Depictio. If you don't find an answer to your question here, please open an issue on [GitHub](https://github.com/depictio/depictio/issues).

## General Questions

### What is Depictio?

Depictio is a microservices web-based platform designed to streamline the analysis of bioinformatics workflows by enabling the creation of customized visualization dashboards. It provides a dynamic and interactive dashboard experience for quality control (QC) metrics monitoring and result exploration in omics.

### Who is Depictio for?

Depictio is designed for bioinformaticians, researchers, and core facilities who work with large-scale omics datasets and need a flexible, interactive way to visualize and analyze their data. The tool is primarily designed to aggregate data from production workflows (e.g., typically [nf-core](https://nf-co.re/)). While the backend is mostly designed to be used by bioinformaticians, the frontend is user-friendly and can be used by anyone who needs to visualize and explore omics data.

### Is Depictio open-source?

Yes, Depictio is an open-source project under MIT Licence. You can find the source code on [GitHub](https://github.com/depictio/depictio).

## Installation and Setup

### What are the system requirements for Depictio?

Depictio is designed to run in containerized environments. The basic requirements are:

- Docker and Docker Compose (for local deployment)
- Kubernetes (for production deployment)

### How do I install Depictio?

Please refer to our [Installation Guide](../installation/install.md) for detailed instructions on how to install Depictio in different environments.

### Can I run Depictio on my local machine?

Yes, you can run Depictio locally using Docker Compose. See the [Docker Compose Installation Guide](../installation/docker.md) for details.

## Usage

### How do I create a dashboard in Depictio?

Creating dashboards in Depictio is straightforward. Please refer to our [Dashboard Creation Guide](../usage/guides/dashboard_creation.md) for step-by-step instructions.

### What data formats does Depictio support?

Depictio currently supports all tabular formats (CSV, TSV, XLSX, Parquet, etc.) compatible with [Polars](https://pola.rs/). Futur versions will include support for [MultiQC](https://seqera.io/multiqc/) reports, as well as [JBrowse](https://jbrowse.org/) compatible omics data formats (BED, BAM, VCF, etc.).

### Can I share my dashboards with others?

Depictio currently supports instance-level sharing of dashboards. You can make your dashboards public or private, and share them with other users on the same instance. Future versions will include more advanced sharing options with role-based access control (RBAC) and user groups. We're also envisioning to support sharing dashboards with external users via public links and via [SciLifeLab Serve](https://serve.scilifelab.se/).

## Technical Questions

### How does Depictio handle large datasets?

Depictio relies on [Polars](https://pola.rs/) and [Delta lake](https://delta.io/) for efficient data processing and storage. This allows it to handle large datasets efficiently, leveraging lazy evaluation and optimized query execution.

### Can I integrate Depictio with my existing workflows?

Yes, Depictio is designed to integrate with existing bioinformatics workflows. The [depictio-CLI](../depictio-cli/usage.md) tool can be used to push data from your workflows to Depictio for visualization.

### Is there an API for Depictio?

Yes, Depictio provides a comprehensive REST API that allows you to interact with all aspects of the platform programmatically. See the [API Reference](../api/reference.md) for details.

## Troubleshooting

### I'm having trouble connecting to the Depictio server. What should I check?

1. Ensure that all required services (API, Dash, MongoDB, MinIO) are running using Docker Compose or Kubernetes
2. Check the logs of the services for any error messages
3. Check network connectivity and firewall settings
4. Verify that the server URLs are correctly configured (in the `.env` file for Docker Compose or in the Kubernetes configuration)

### How do I report a bug or request a feature?

You can report bugs or request features by opening an issue on our [GitHub repository](https://github.com/depictio/depictio/issues). Please provide as much detail as possible to help us understand and address your issue.
