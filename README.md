
# FinBERT Flask App Deployment Guide

This guide provides step-by-step instructions for deploying the FinBERT Flask App on AWS EKS using `eksctl` and setting up a CI/CD pipeline with GitHub Actions.

## Prerequisites

- AWS account with appropriate permissions.
- AWS CLI installed and configured.
- `eksctl` and `kubectl` tools installed.
- GitHub account and repository for the app.

## Step 1: AWS CLI Configuration

- Install and configure the AWS CLI:
  ```bash
  aws configure
  ```
- Enter your AWS Access Key ID, Secret Access Key, region, and output format.

## Step 2: Create an ECR Repository

- Create a new ECR repository to store your Docker images:
  ```bash
  aws ecr create-repository --repository-name finbert-flask-app
  ```

## Step 3: Create an IAM User for GitHub Actions

- Create an IAM user with programmatic access and necessary permissions for ECR and EKS.
- Note down the Access Key ID and Secret Access Key.

## Step 4: EKS Cluster Setup Using eksctl

- To create your EKS cluster, use the following `eksctl` commands (as specified in your provided files):
  ```bash
  eksctl create cluster --name finbert-cluster --version 1.17 --region us-west-2 --nodegroup-name linux-nodes --node-type t2.micro --nodes 2
  ```
- For additional configuration and options, refer to the [eksctl documentation](https://eksctl.io/).

### Deleting Deployments and Services

- To delete specific deployments or services in your cluster:
  ```bash
  kubectl delete deployment <deployment-name>
  kubectl delete service <service-name>
  ```

### Deleting the EKS Cluster

- To delete your EKS cluster:
  ```bash
  eksctl delete cluster --name finbert-cluster
  ```

## Step 5: Configure GitHub Secrets

- Go to your GitHub repository > Settings > Secrets.
- Add the following secrets:
  - `AWS_ACCESS_KEY_ID`: The Access Key ID of the IAM user.
  - `AWS_SECRET_ACCESS_KEY`: The Secret Access Key of the IAM user.
  - `AWS_REGION`: Your AWS region.
  - `ECR_REPOSITORY`: Name of the ECR repository.

## Step 6: GitHub Actions Workflow

- Create a `.github/workflows` directory in your repository.
- Add a workflow file (e.g., `ci-cd.yml`).
- Define steps for building, pushing the Docker image, and deploying to EKS.

## Step 7: Deploying the Application

- Push changes to your repository.
- GitHub Actions will build the Docker image and deploy it to EKS.

## Additional Information

- Ensure to follow the best practices for AWS ECR and IAM setup as outlined in the [AWS documentation](https://aws.amazon.com/documentation/).
