
# FinBERT Flask App Deployment Guide

This guide provides step-by-step instructions for productionalizing this FinBERT Flask App on AWS EKS using `eksctl` to setup the kubernetes cluster on EKS and setting up a CI/CD pipeline with GitHub Actions.

## Prerequisites

- AWS account with appropriate permissions.
    - Review this document for required permissions on EKS: [https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonelastickubernetesservice.html)
- `aws` CLI installed and configured.
    - Getting started with `aws` CLI: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - Quick configuration guide: [https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-configure-quickstart-config](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-configure-quickstart-config)
- `eksctl` and `kubectl` tools installed.
    - Getting started with `eksctl`: [https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)
    - Getting started with `kubectl`: [https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
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
  eksctl create cluster --name finbert-cluster --region us-east-1 --node-type t3.small --node-ami-family Ubuntu2004 --nodes-min 2 --nodes-max 3 # --dry-run # uncomment to do a dry run to validate the cluster config
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

## Step 5: Configure GitHub Secrets/Variables

- Go to your GitHub repository > Settings > Secrets.
- Add the following secrets:
  - `AWS_ACCESS_KEY_ID`: The Access Key ID of the IAM user.
  - `AWS_SECRET_ACCESS_KEY`: The Secret Access Key of the IAM user.
- Add the following variables:
  - `AWS_REGION`: Your AWS region.
  - `ECR_REPOSITORY`: Name of the ECR repository.
  - `EKS_CLUSTER_NAME`: Name of the EKS cluster.

## Step 6: GitHub Actions Workflow

- Create a `.github/workflows` directory in your repository.
- Add a workflow file (e.g., `ci-cd.yml`).
- Define steps for building, pushing the Docker image, and deploying to EKS.

## Step 7: Deploying the Application

- Push changes to your repository.
- GitHub Actions will build the Docker image and deploy it to EKS.

## Additional Information

- `eksctl` creates a CloudFormation stack for the EKS cluster, which can be viewed in the CloudFormation console or addtionally one could use cf2tf to convert the CloudFormation stack to Terraform code.
- Link to cf2tf - https://github.com/DontShaveTheYak/cf2tf