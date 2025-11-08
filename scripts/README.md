# Deployment Scripts

Scripts to help deploy the Prompt Firewall to GCP Cloud Run.

## Scripts

### `setup-gcp.sh` / `setup-gcp.ps1`
Sets up GCP project, creates Cloud SQL database, and configures secrets.

**Usage:**
```bash
export PROJECT_ID="your-project-id"
./scripts/setup-gcp.sh
```

### `deploy-backend.sh` / `deploy-backend.ps1`
Builds Docker image and deploys backend to Cloud Run.

**Usage:**
```bash
export PROJECT_ID="your-project-id"
export CORS_ORIGINS="https://your-frontend-url.com"  # Optional
./scripts/deploy-backend.sh
```

### `run-migrations.sh`
Runs database migrations using Cloud Run Jobs.

**Usage:**
```bash
export PROJECT_ID="your-project-id"
./scripts/run-migrations.sh
```

### `init-db.sh`
Initializes database with default admin users and policy rules.

**Usage:**
```bash
export PROJECT_ID="your-project-id"
./scripts/init-db.sh
```

## Quick Deploy

See [QUICK_DEPLOY.md](../QUICK_DEPLOY.md) for a complete step-by-step guide.

## Prerequisites

- GCP account with billing enabled
- `gcloud` CLI installed and authenticated
- `docker` installed
- Environment variable `PROJECT_ID` set

