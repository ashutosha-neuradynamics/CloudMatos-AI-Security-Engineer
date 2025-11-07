# Database Scripts

## create_test_admin.py

Creates a test admin user with known credentials for development and testing.

**Usage:**
```bash
# With Docker Compose
docker-compose exec backend python scripts/create_test_admin.py

# Or locally
python scripts/create_test_admin.py
```

**Default Test Credentials:**
- Username: `testadmin`
- Password: `test123`

**Note:** This script will not overwrite an existing user. If the test admin already exists, it will display a message and exit.

