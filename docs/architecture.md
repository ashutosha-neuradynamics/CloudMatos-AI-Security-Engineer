# Architecture Overview - Prompt Firewall

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐         ┌──────────────┐                    │
│  │   Demo UI    │         │ Admin Console│                    │
│  │  (Next.js)   │         │  (Next.js)   │                    │
│  └──────┬───────┘         └──────┬───────┘                    │
│         │                         │                             │
│         │  HTTPS                  │  HTTPS + Auth              │
└─────────┼─────────────────────────┼─────────────────────────────┘
          │                         │
          │                         │
┌─────────▼─────────────────────────▼─────────────────────────────┐
│                      API Gateway Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FastAPI Backend (Cloud Run)                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Query   │  │  Policy  │  │   Logs   │            │   │
│  │  │ Endpoint │  │ Endpoint  │  │ Endpoint │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼─────────────┼──────────────┼───────────────────────┘   │
│          │             │             │                           │
│          └─────────────┼─────────────┘                           │
│                        │                                         │
│          ┌─────────────▼─────────────┐                          │
│          │    Firewall Engine        │                          │
│          │  ┌─────────────────────┐  │                          │
│          │  │  PII Detector       │  │                          │
│          │  │  Injection Detector │  │                          │
│          │  │  Policy Engine      │  │                          │
│          │  └─────────────────────┘  │                          │
│          └──────────────────────────┘                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Encrypted Connection
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      Data Layer                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Cloud SQL       │         │  Secret Manager  │            │
│  │  PostgreSQL      │         │  (Secrets)       │            │
│  │                  │         │                  │            │
│  │  - Request Logs  │         │  - DB Password  │            │
│  │  - Policy Rules  │         │  - JWT Secret    │            │
│  │  - Admin Users   │         │  - API Keys      │            │
│  │  - Audit Trail   │         │                  │            │
│  └──────────────────┘         └──────────────────┘            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Integration Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Python SDK                                  │   │
│  │  - API Client Wrapper                                    │   │
│  │  - Error Handling                                        │   │
│  │  - Type Definitions                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js)
- **Demo UI**: Public-facing interface for testing firewall
- **Admin Console**: Authenticated interface for policy and log management
- **Technology**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Deployment**: Vercel or Cloud Run

### Backend API (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **Endpoints**:
  - `/v1/query` - Process prompts/responses
  - `/v1/policy` - Policy management
  - `/v1/logs` - Log retrieval
  - `/v1/auth/login` - Authentication
  - `/v1/health` - Health check
- **Deployment**: Cloud Run (serverless)
- **Scaling**: Auto-scaling 0-10 instances

### Firewall Engine
- **PII Detector**: Regex-based detection for emails, SSNs, phones, etc.
- **Injection Detector**: Pattern matching for jailbreak attempts
- **Policy Engine**: Rule-based decision making (block/redact/warn/allow)
- **Processing**: Synchronous, <500ms typical latency

### Database (PostgreSQL)
- **Instance**: Cloud SQL PostgreSQL 15
- **Tables**:
  - `request_logs` - All processed requests
  - `policy_rules` - Security rules
  - `admin_users` - Admin accounts
  - `audit_logs` - Admin actions
- **Backup**: Automated daily backups

### Security
- **Authentication**: JWT tokens
- **Secrets**: Google Secret Manager
- **Encryption**: TLS in transit, encryption at rest
- **Network**: Private IP for database, public API with CORS

## Data Flow

### 1. Query Processing Flow
```
User Input → Frontend → API Gateway → Firewall Engine
                                         ↓
                                    PII Detection
                                         ↓
                                    Injection Detection
                                         ↓
                                    Policy Engine
                                         ↓
                                    Decision (Block/Redact/Warn/Allow)
                                         ↓
                                    Log to Database
                                         ↓
                                    Return Response → Frontend → User
```

### 2. Admin Flow
```
Admin → Login → JWT Token → Admin Console
                                    ↓
                            Policy Management
                                    ↓
                            Update Policy Rules
                                    ↓
                            Save to Database
                                    ↓
                            Audit Log Entry
```

### 3. Log Retrieval Flow
```
Admin → Admin Console → API (Authenticated)
                            ↓
                    Query Database
                            ↓
                    Apply Filters
                            ↓
                    Paginate Results
                            ↓
                    Return Logs → Admin Console
```

## Technology Stack

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.104
- **Database**: PostgreSQL (via SQLAlchemy)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: python-jose (JWT)
- **Password Hashing**: passlib (bcrypt)
- **HTTP Client**: httpx (for SDK)

### Frontend
- **Framework**: Next.js 16
- **Language**: TypeScript
- **UI**: React 19
- **Styling**: Tailwind CSS 4
- **HTTP Client**: Fetch API

### Infrastructure
- **Compute**: Google Cloud Run
- **Database**: Google Cloud SQL
- **Secrets**: Google Secret Manager
- **IaC**: Terraform
- **Container**: Docker

### SDK
- **Language**: Python 3.8+
- **HTTP Client**: httpx
- **Package Manager**: setuptools

## Deployment Architecture

### Production Deployment
```
Internet
   │
   ├─→ Cloud Load Balancer (optional)
   │
   ├─→ Cloud Run (Backend)
   │   └─→ Cloud SQL (Private IP)
   │
   └─→ Vercel/Cloud Run (Frontend)
       └─→ API Calls to Backend
```

### Development Environment
```
Local Machine
   │
   ├─→ Backend (localhost:8000)
   │   └─→ Local PostgreSQL
   │
   └─→ Frontend (localhost:3000)
       └─→ API Calls to localhost:8000
```

## Security Boundaries

1. **Public Internet ↔ Frontend**: HTTPS, CORS
2. **Frontend ↔ Backend**: HTTPS, API authentication
3. **Backend ↔ Database**: Private network, encrypted
4. **Admin ↔ Admin Console**: JWT authentication
5. **SDK ↔ Backend**: API key (optional), HTTPS

## Scalability

- **Horizontal Scaling**: Cloud Run auto-scales based on traffic
- **Database**: Can upgrade Cloud SQL tier for higher load
- **Caching**: Can add Redis for policy caching (future)
- **CDN**: Frontend assets can be served via CDN

## Monitoring & Observability

- **Logging**: Cloud Logging (structured logs)
- **Metrics**: Cloud Run metrics (requests, latency, errors)
- **Tracing**: Can integrate with Cloud Trace
- **Alerts**: Cloud Monitoring alerts

## Cost Optimization

- **Serverless**: Pay per request (Cloud Run)
- **Database**: Smallest tier for MVP
- **Scaling to Zero**: No cost when idle
- **CDN**: Cache static assets

---

**Last Updated**: 2024
**Version**: 1.0

