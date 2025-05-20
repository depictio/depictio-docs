# Kubernetes Installation

This guide will walk you through deploying Depictio on a Kubernetes cluster using Helm charts.

## Prerequisites

Before you begin, ensure you have:

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure (if persistence is enabled)

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
```

### Step 2: Install the Chart

To install the chart with the release name `depictio`:

```bash
helm install depictio ./helm-charts/depictio
```

This command deploys Depictio on the Kubernetes cluster with the default configuration.

### Step 3: Verify the Installation

Check that all pods are running:

```bash
kubectl get pods -n datasci-depictio-project
```

You should see pods for the backend, frontend, MongoDB, and MinIO.

## Accessing Depictio

After deploying the chart, you can access the Depictio application:

- If using ClusterIP (default), use port-forwarding to access the frontend service:

```bash
kubectl port-forward -n datasci-depictio-project service/depictio-frontend 5080:80
```

Then visit <http://localhost:5080> in your browser.

## Customizing the Installation

You can customize the chart by overriding its values in a separate YAML file:

```bash
helm install depictio ./helm-charts/depictio -f my-values.yaml
```

For a complete list of configurable parameters, refer to the `values.yaml` file or run:

```bash
helm show values ./helm-charts/depictio
```

## Uninstalling

To uninstall/delete the `depictio` deployment:

```bash
helm uninstall depictio
```

## Key Configuration Parameters

Here are some of the key parameters you can configure:

### Storage

The chart supports persistence for various components:

- MongoDB data
- MinIO storage
- Screenshots
- Example data

By default, all persistence is enabled with appropriate storage sizes.

### Services

- Backend API: Accessible on port 8058
- Frontend: Accessible on port 5080
- MongoDB: Accessible on port 27018
- MinIO: Accessible on ports 9000 (API) and 9001 (Console)

For more detailed configuration options, please refer to the [Helm chart README](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/README.md).
