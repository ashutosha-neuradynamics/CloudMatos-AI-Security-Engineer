# Deployment Guide - Prompt Firewall

This guide covers deploying the Prompt Firewall application to Google Cloud Platform.

## Prerequisites

- Google Cloud Platform account with billing enabled
- `gcloud` CLI installed and configured
- `docker` installed (for building images)
- `docker-compose` installed (for local development)
- `terraform` installed (optional, for infrastructure as code)

## Local Development with Docker Compose

For local development, you can use Docker Compose to run the backend and database:

```bash
# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Initialize database with default data
docker-compose exec backend python -m app.init_db

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

The backend will be available at http://localhost:8000 with hot-reload enabled.

**Default Admin Credentials:**
- **Admin**: `admin` / `admin123`
- **Test Admin**: `testadmin` / `test123`

You can use these credentials to login to the admin console at http://localhost:3000/admin/login

## Architecture Overview

The application consists of:
- **Backend API**: FastAPI application running on Cloud Run
- **Frontend**: Next.js application (can be deployed to Vercel, Cloud Run, or Cloud Storage)
- **Database**: Cloud SQL PostgreSQL instance
- **Secrets**: Google Secret Manager

## Estimated Monthly Costs

For low to moderate traffic (< 10,000 requests/day):

- **Cloud Run (Backend)**: ~$5-15/month
  - CPU: 0.1 vCPU average
  - Memory: 256MB average
  - Requests: ~300K/month
  
- **Cloud SQL (PostgreSQL)**: ~$7-10/month
  - db-f1-micro instance
  - 10GB storage
  
- **Secret Manager**: ~$0.06/month
  - 2 secrets
  
- **Cloud Build**: ~$1-5/month (if using CI/CD)
  
- **Frontend Hosting (Vercel)**: Free tier or ~$20/month (Pro)

**Total Estimated Cost: $15-50/month** for MVP scale

## Step 1: Set Up GCP Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com
```

## Step 2: Create Database

### Option A: Using Terraform

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

### Option B: Manual Setup

```bash
# Create Cloud SQL instance
gcloud sql instances create prompt-firewall-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_ROOT_PASSWORD

# Create database
gcloud sql databases create prompt_firewall \
  --instance=prompt-firewall-db

# Create user
gcloud sql users create app_user \
  --instance=prompt-firewall-db \
  --password=YOUR_DB_PASSWORD
```

## Step 3: Set Up Secrets

```bash
# Create secrets
echo -n "postgresql://app_user:PASSWORD@/prompt_firewall?host=/cloudsql/PROJECT_ID:REGION:prompt-firewall-db" | \
  gcloud secrets create database-url --data-file=-

echo -n "your-secret-key-change-in-production" | \
  gcloud secrets create secret-key --data-file=-
```

## Step 4: Build and Deploy Backend

```bash
cd backend

# Build Docker image
docker build -t gcr.io/$PROJECT_ID/prompt-firewall-backend:latest .

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/prompt-firewall-backend:latest

# Deploy to Cloud Run
gcloud run deploy prompt-firewall-backend \
  --image gcr.io/$PROJECT_ID/prompt-firewall-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars CORS_ORIGINS="https://YOUR_FRONTEND_URL" \
  --add-cloudsql-instances $PROJECT_ID:us-central1:prompt-firewall-db \
  --set-secrets DATABASE_URL=database-url:latest,SECRET_KEY=secret-key:latest
```

## Step 5: Deploy Frontend

### Option A: Deploy to Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_URL=https://YOUR_BACKEND_URL`
3. Deploy

### Option B: Deploy to Cloud Run

```bash
cd frontend

# Build Next.js app
npm run build

# Create Dockerfile for production
# (You'll need to create a Dockerfile that serves the Next.js app)

# Build and deploy
docker build -t gcr.io/$PROJECT_ID/prompt-firewall-frontend:latest .
docker push gcr.io/$PROJECT_ID/prompt-firewall-frontend:latest

gcloud run deploy prompt-firewall-frontend \
  --image gcr.io/$PROJECT_ID/prompt-firewall-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://YOUR_BACKEND_URL
```

## Step 6: Initialize Database

```bash
# Connect to Cloud SQL and run migrations
gcloud sql connect prompt-firewall-db --user=postgres

# Or use Cloud SQL Proxy
cloud_sql_proxy -instances=$PROJECT_ID:us-central1:prompt-firewall-db=tcp:5432

# Run migrations
cd backend
alembic upgrade head

# Initialize database with default data
python -m app.init_db
```

## Step 7: Configure CORS

Update the backend CORS_ORIGINS environment variable to include your frontend URL:

```bash
gcloud run services update prompt-firewall-backend \
  --update-env-vars CORS_ORIGINS="https://YOUR_FRONTEND_URL" \
  --region us-central1
```

## Step 8: Set Up Custom Domain (Optional)

```bash
# Map custom domain to Cloud Run service
gcloud run domain-mappings create \
  --service prompt-firewall-backend \
  --domain api.yourdomain.com \
  --region us-central1
```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `ALGORITHM`: JWT algorithm (default: HS256)

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Monitoring and Logging

### View Logs

```bash
# Backend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=prompt-firewall-backend" --limit 50

# Frontend logs (if on Cloud Run)
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=prompt-firewall-frontend" --limit 50
```

### Set Up Alerts

1. Go to Cloud Console > Monitoring > Alerting
2. Create alert policies for:
   - High error rate
   - High latency
   - Low availability

## Troubleshooting

### Database Connection Issues

- Verify Cloud SQL instance is running
- Check Cloud Run service has Cloud SQL connection configured
- Verify database credentials in Secret Manager

### CORS Errors

- Ensure CORS_ORIGINS includes your frontend URL
- Check that backend allows credentials if needed

### High Costs

- Review Cloud Run instance scaling settings
- Consider reducing max instances
- Use Cloud SQL smaller tier if traffic is low

## Scaling

For higher traffic:
- Increase Cloud Run max instances
- Upgrade Cloud SQL tier
- Enable Cloud CDN for static assets
- Consider using Cloud Load Balancer

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use Secret Manager** for all sensitive data
3. **Enable Cloud Armor** for DDoS protection
4. **Use IAM** to restrict access
5. **Enable audit logging**
6. **Regularly rotate secrets**
7. **Use HTTPS only**

## Backup and Recovery

### Database Backups

Cloud SQL automatically creates daily backups. To restore:

```bash
gcloud sql backups restore BACKUP_ID \
  --backup-instance=prompt-firewall-db
```

### Manual Backup

```bash
gcloud sql export sql prompt-firewall-db gs://YOUR_BUCKET/backup-$(date +%Y%m%d).sql \
  --database=prompt_firewall
```

## CI/CD Setup (Optional)

See `.github/workflows/` for GitHub Actions workflows that can:
- Build and test on PR
- Deploy to Cloud Run on merge to main
- Run database migrations

## Cost Optimization Tips

1. Use Cloud Run min instances = 0 (scales to zero)
2. Use smallest Cloud SQL tier for MVP
3. Enable Cloud Run CPU throttling
4. Use Cloud CDN for static assets
5. Monitor and set budget alerts

## Support

For issues or questions:
- Check logs in Cloud Console
- Review Cloud Run metrics
- Check database connection status
- Verify secrets are accessible

