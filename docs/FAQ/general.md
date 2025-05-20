# Frequently Asked Questions

This page addresses common questions about Depictio. If you don't find an answer to your question here, please check our community forums or open an issue on GitHub.

## General Questions

### What is Depictio?

Depictio is a microservices web-based platform designed to streamline the analysis of bioinformatics workflows by enabling the creation of customized visualization dashboards. It provides a dynamic and interactive dashboard experience for quality control (QC) metrics monitoring and result exploration in omics.

### Who is Depictio for?

Depictio is designed for bioinformaticians, researchers, and core facilities who work with large-scale omics datasets and need a flexible, interactive way to visualize and analyze their data.

### Is Depictio open-source?

Yes, Depictio is an open-source project. You can find the source code on [GitHub](https://github.com/depictio/depictio).

## Installation and Setup

### What are the system requirements for Depictio?

Depictio is designed to run in containerized environments. The basic requirements are:

- Docker and Docker Compose (for local deployment)
- Kubernetes (for production deployment)
- Sufficient storage for your data

### How do I install Depictio?

Please refer to our [Installation Guide](../installation/install.md) for detailed instructions on how to install Depictio in different environments.

### Can I run Depictio on my local machine?

Yes, you can run Depictio locally using Docker Compose. See the [Docker Compose Installation Guide](../installation/docker.md) for details.

## Usage

### How do I create a dashboard in Depictio?

Creating dashboards in Depictio is straightforward. Please refer to our [Dashboard Creation Guide](../usage/guides/dashboard_creation.md) for step-by-step instructions.

### What data formats does Depictio support?

Depictio supports a variety of data formats, including:

- Standard tabular formats (CSV, TSV, XLSX, Parquet)
- Genome-browser compatible data formats (BED, BigBed, BigWig, BAM/CRAM, VCF)

### Can I share my dashboards with others?

Yes, Depictio allows you to share dashboards with other users. You can control access permissions to determine who can view or edit your dashboards.

## Technical Questions

### How does Depictio handle large datasets?

Depictio is designed with scalability in mind. It uses efficient data storage and retrieval mechanisms, and its microservices architecture allows for horizontal scaling to handle large datasets.

### Can I integrate Depictio with my existing workflows?

Yes, Depictio is designed to integrate with existing bioinformatics workflows. The CLI tool allows you to push data from your workflows to Depictio for visualization.

### Is there an API for Depictio?

Yes, Depictio provides a comprehensive REST API that allows you to interact with all aspects of the platform programmatically. See the [API Reference](../api/overview.md) for details.

## Troubleshooting

### I'm having trouble connecting to the Depictio server. What should I check?

1. Ensure that all required services (API, Dash, MongoDB, MinIO) are running
2. Check network connectivity and firewall settings
3. Verify that the server URLs are correctly configured
4. Check the logs for any error messages

### How do I report a bug or request a feature?

You can report bugs or request features by opening an issue on our [GitHub repository](https://github.com/depictio/depictio/issues). Please provide as much detail as possible to help us understand and address your issue.
