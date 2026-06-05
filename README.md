# secure-commerce-data-pipeline
An automated e-commerce data platform demonstrating infrastructure-as-code (AWS CDK), pipeline reliability, and secure backend data transformations in Python.

# Secure Commerce Data Pipeline 🚀

A production-grade, cloud-native data ingestion pipeline engineered to demonstrate robust ETL practices, Infrastructure as Code (IaC), and automated data sanitization. 

This project simulates a secure e-commerce data platform that automatically ingests raw user and transactional data from a public REST API, validates its processing integrity, masks sensitive Personal Identifiable Information (PII), and stores it securely in a cloud data lake.

---

## 🏗️ Architectural Design (Target State)

* **Ingestion Layer:** Python-based ingestion engine running via AWS Lambda to fetch high-volume transactional data.
* **Security & Compliance Layer:** Shift-left DevSecOps processing that automatically scans, hashes, and masks sensitive user metadata (emails, phone numbers, and geolocation metrics) prior to persistent storage.
* **Infrastructure as Code (IaC):** 100% defined, isolated, and deployed via **AWS CDK (TypeScript)**.
* **Storage Layer:** Partitioned, compliance-mapped data storage utilizing **AWS S3** and **AWS DynamoDB**.
* **Observability & Reliability:** Structured logging and validation suites to track pipeline health and prevent data definition drift.

---

## 🛠️ Technical Toolkit

* **Languages:** Python 3.x, TypeScript (for AWS CDK), SQL
* **Cloud Infrastructure:** AWS CDK, AWS Lambda, AWS S3, DynamoDB
* **Engineering Practices:** Test-Driven Development (TDD), DevSecOps, Automated PII Anonymization, Structural Threat Modeling (STRIDE)
* **Quality Assurance:** Python `unittest` framework for transformation logic validation

---

## 📈 Project Roadmap & Status

- [X] Repository initialized & architecture planned
- [X] Local Python ingestion script & API connection
- [X] Core PII Masking and Data Validation logic suites
- [X] AWS CDK Infrastructure definition & IAM least-privilege scoping
- [X] Unit testing implementation & GitHub Actions CI/CD setup

---
*Developed as a showcase of secure, enterprise-grade cloud data engineering patterns.*
