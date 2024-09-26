---
hide:
  - title
  - navigation
  - toc
---
<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>



<p align="center">
  <img src="./images/logo/logo_hd.png" alt="Depictio logo" width=300>
</p>


![](./images/Demo.gif)




## Project Overview

Depictio is an innovative microservices web-based platform designed to streamline the analysis of bioinformatics workflows by enabling the creation of customized visualization dashboards using various type of  outputs compatible with the platform. It provides a dynamic and interactive dashboard experience for quality control (QC) metrics monitoring and result exploration in omics. The platform is tailored towards large-scale studies and research facilities, offering support for various data formats and interactive data visualization tools.



## Features

* Dynamic Dashboards: Real-time data interaction, customizable views, and user-driven exploration features.
* Diverse Data Format Support: Handles standard formats like CSV, TSV, XLSX, Parquet, and omics files like BED, BigBed, BigWig, BAM/CRAM, VCF.
* Robust Backend Technologies: Utilizes FastAPI, MongoDB, and Redis cache for high-performance data management and processing.
* Intuitive Frontend: Built on Plotly Dash, a ReactJS-based framework


## Architecture


<p align="center">
  <img src="./images/main.png" alt="Depictio logo" width=800>
</p>


Depictio architecture is composed of a microservices architecture, including 6 microservices currently:

1. FastAPI instance

2. mongoDB database

3. redis cache system

4. JBrowse on-premise genome browser

5. MinIO S3 bucket management instance

6. Plotly Dash server

<!-- 

## Current Status

!!! warning
   
      * Depictio is currently in the development phase and is not yet available for general use. The platform is being built with an emphasis on versatility and adaptability to various biological research needs. -->
