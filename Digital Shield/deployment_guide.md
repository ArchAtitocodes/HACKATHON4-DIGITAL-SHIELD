# Digital Shield - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker (recommended) OR Python 3.10+
- Git (optional, for cloning)

---

## Method 1: Docker Deployment (Recommended)

### Step 1: Build the Docker Image
```bash
docker build -t digital-shield:latest .
```

### Step 2: Run the Container
```bash
docker run -d \
  --name digital-shield \
  -p 5000:5000 \
  --restart unless-stopped \
  digital-shield:latest
```

### Step 3: Verify Deployment
```bash
# Check container status
docker ps

# View logs
docker logs digital-shield

# Test health endpoint
curl http://localhost:5000/health
```

### Step 4: Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

### Managing the Container
```bash
# Stop the container
docker stop digital-shield

# Start the container
docker start digital-shield

# Restart the container
docker restart digital-shield

# Remove the container
docker rm -f digital-shield

# View real-time logs
docker logs -f digital-shield
```

---

## Method 2: Local Development (Without Docker)

### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
# Development mode
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py

# Production mode with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
```

### Step 4: Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

---

## Method 3: Cloud Deployment

### Deploy to Render

1. **Create a new Web Service on Render.com**
2. **Connect your Git repository**
3. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment:** Python 3.10

### Deploy to Railway

1. **Create a new project on Railway.app**
2. **Connect your Git repository**
3. **Railway auto-detects the Dockerfile**
4. **Deploy automatically**

### Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login to Fly.io
flyctl auth login

# Launch the app
flyctl launch

# Deploy
flyctl deploy
```

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create digital-shield-app

# Set environment
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Environment Variables

### Required
None (app uses secure defaults)

### Optional
```bash
# Flask Configuration
FLASK_ENV=production           # production or development
SECRET_KEY=your-secret-key     # Flask secret key (auto-generated if not set)

# Server Configuration
PORT=5000                      # Port to run on (default: 5000)
WORKERS=2                      # Number of gunicorn workers (default: 2)
```

### Setting Environment Variables

**Docker:**
```bash
docker run -d \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -p 5000:5000 \
  digital-shield:latest
```

**Local:**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

---

## Health Checks & Monitoring

### Health Check Endpoint
```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Digital Shield",
  "data_files": {
    "scenarios": true,
    "literacy": true
  },
  "active_sessions": 0
}
```

### Monitoring
- Monitor the `/health` endpoint for service status
- Check `active_sessions` count to monitor usage
- Review logs for errors

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
docker run -p 8080:5000 digital-shield:latest
```

### Container Won't Start
```bash
# Check logs
docker logs digital-shield

# Verify data files exist
docker exec digital-shield ls -la data/
```

### JSON Files Not Found
```bash
# Ensure data directory structure is correct:
# data/scenarios.json
# data/literacy.json

# Verify in container
docker exec digital-shield cat data/scenarios.json
```

### Session Issues
- Sessions expire after 5 minutes of inactivity (by design)
- No data persists beyond session lifetime (privacy feature)
- If users report unexpected session ends, check server logs

---

## Security Considerations

### Production Checklist
- ✅ Generate a strong SECRET_KEY
- ✅ Enable HTTPS (use reverse proxy like Nginx)
- ✅ Set FLASK_ENV=production
- ✅ Keep dependencies updated
- ✅ Monitor logs for suspicious activity
- ✅ Use firewall rules to restrict access if needed

### HTTPS Setup (with Nginx)
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Performance Optimization

### Gunicorn Workers
Rule of thumb: `(2 × CPU cores) + 1`

```bash
# For 2 CPU cores
gunicorn --workers 5 --bind 0.0.0.0:5000 app:app

# For 4 CPU cores
gunicorn --workers 9 --bind 0.0.0.0:5000 app:app
```

### Docker Resource Limits
```bash
docker run -d \
  --memory="512m" \
  --cpus="1.0" \
  -p 5000:5000 \
  digital-shield:latest
```

---

## Backup & Disaster Recovery

### Data Files
The only persistent data is in `data/*.json` files:
- `data/scenarios.json`
- `data/literacy.json`

**Backup:**
```bash
# Create backup
cp -r data/ data-backup-$(date +%Y%m%d)/

# From Docker container
docker cp digital-shield:/app/data ./data-backup
```

**Restore:**
```bash
# To Docker container
docker cp ./data-backup/scenarios.json digital-shield:/app/data/
docker restart digital-shield
```

---

## Scaling

### Horizontal Scaling
Deploy multiple instances behind a load balancer:

```bash
# Start multiple containers
docker run -d --name digital-shield-1 -p 5001:5000 digital-shield:latest
docker run -d --name digital-shield-2 -p 5002:5000 digital-shield:latest
docker run -d --name digital-shield-3 -p 5003:5000 digital-shield:latest
```

### Load Balancer (Nginx)
```nginx
upstream digital_shield {
    server localhost:5001;
    server localhost:5002;
    server localhost:5003;
}

server {
    listen 80;
    location / {
        proxy_pass http://digital_shield;
    }
}
```

---

## Testing Deployment

### Automated Tests
```bash
# Test health endpoint
curl -f http://localhost:5000/health || exit 1

# Test scenarios endpoint
curl -f http://localhost:5000/api/chatbot/scenarios || exit 1

# Test literacy platforms
curl -f http://localhost:5000/api/literacy/platforms || exit 1
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/
```

---

## Support & Maintenance

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker build -t digital-shield:latest .

# Restart with new image
docker stop digital-shield
docker rm digital-shield
docker run -d --name digital-shield -p 5000:5000 digital-shield:latest
```

### Logs
```bash
# View application logs
docker logs digital-shield

# Follow logs in real-time
docker logs -f digital-shield

# Save logs to file
docker logs digital-shield > app.log 2>&1
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Build image | `docker build -t digital-shield .` |
| Run container | `docker run -d -p 5000:5000 digital-shield` |
| Stop container | `docker stop digital-shield` |
| View logs | `docker logs digital-shield` |
| Check health | `curl http://localhost:5000/health` |
| Run locally | `python app.py` |
| Production run | `gunicorn --bind 0.0.0.0:5000 app:app` |

---

## Developer Information

**Developed by:** Eng. Stephen Odhiambo  
**Role:** Kenyan AI Engineer & Software Engineer  
**Project:** Digital Shield MVP - TFGBV Response Tool  
**License:** Open Source (specify your license)  
**Contact:** [Add your contact information]

---

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Docker Documentation: https://docs.docker.com/
- Gunicorn Documentation: https://docs.gunicorn.org/
- Security Best Practices: https://owasp.org/

---

**🛡️ Digital Shield - Protecting Women and Girls in African Digital Spaces**