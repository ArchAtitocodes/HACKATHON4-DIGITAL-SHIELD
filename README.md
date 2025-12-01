# 🛡️ Digital Shield

## Technology-Facilitated Gender-Based Violence (TFGBV) Response Tool

[![License](https://img.shields.io/badge/license-Open%20Source-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

**Digital Shield** is a rapid-response web application providing safe, private support for women and girls facing online harassment, cyberstalking, and image-based abuse in African digital spaces. *Digital Shield*, is a rapid-response tool addressing **Technology-Facilitated Gender-Based Violence (TFGBV)** in African digital spaces.

---

## 📌 Quick Links

1. **GitHub:** [ArchAtitocodes](https://github.com/ArchAtitocodes)

2.  **Project Repository:** [HACKATHON4-DIGITAL-SHIELD] (https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD.git)

3. **LIVE DEMO LINK:**[DIGITAL-SHIELD]()

4. **VIEW LIVE PITCH DECK LINK ON CANVA:**[DIGITAL-SHIELD] https://www.canva.com/design/DAG5OI5gn6U/oJ207IsDXplVpiwngNLG5g/edit?utm_content=DAG5OI5gn6U&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Deployment Guide](#-deployment-guide)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Design Principles](#-design-principles)
- [Security & Privacy](#-security--privacy)
- [Performance](#-performance)
- [Localization](#-localization)
- [File Manifest](#-file-manifest)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [Support Resources](#-support-resources)
- [Developer Information](#-developer-information)

---

## 🎯 Project Overview

### Problem Statement

Women and girls across Africa face increasing digital harm:
- **Image-based abuse** (revenge porn, deepfakes)
- **Cyberstalking** (repeated unwanted contact, monitoring)
- **Online harassment** (threats, coordinated attacks)

Existing solutions often require:
- Personal data sharing
- Complex navigation
- High technical literacy
- External dependencies

### Our Solution

Digital Shield provides:
✅ **Emergency triage chatbot** - Step-by-step crisis guidance  
✅ **Platform safety checklists** - Practical security steps for WhatsApp, Facebook, Instagram, Twitter, TikTok  
✅ **Complete privacy** - No data collection, no logs, ephemeral sessions  
✅ **Mobile-first design** - Works on low-end devices, 3G networks  
✅ **Culturally sensitive** - Designed for African digital contexts  

---

## 🔑 Key Features

### 1. Emergency Triage Chatbot

- **Finite State Machine (FSM)** for predictable, safe navigation
- **Three TFGBV scenarios:**
  - Image-based abuse
  - Cyberstalking
  - Online harassment
- **Privacy-by-design:**
  - No PII collection
  - In-memory sessions only
  - Auto-expire after 5 minutes
- **Actionable output:**
  - Immediate protective steps
  - Evidence collection guidance
  - Support contacts and legal resources

### 2. Digital Literacy Guide

- **Platform-specific checklists** for:
  - WhatsApp
  - Facebook
  - Instagram
  - Twitter/X
  - TikTok
- **Step-by-step instructions** with visual indicators
- **Localization-ready** JSON structure
- **Resource directory** with helplines and organizations

### 3. Security & Privacy

- **Zero data collection** - no names, emails, IPs, device IDs
- **Ephemeral sessions** - auto-delete on close or timeout
- **Content Security Policy (CSP)** headers
- **XSS protection** with input sanitization
- **HTTPS-ready** for production deployment

### 4. Accessibility

- **WCAG 2.1 Level AA** compliant
- **Semantic HTML** structure
- **ARIA labels** for screen readers
- **High contrast** UI elements
- **Keyboard navigation** support
- **Mobile-first** responsive design (320px+)

---

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Backend** | Python (Flask) | Lightweight, secure, rapid development |
| **Frontend** | HTML5, CSS3, Vanilla JS | No dependencies, fast loading, universal compatibility |
| **Data Storage** | JSON flat files | Simple, portable, no database overhead |
| **Deployment** | Docker | Consistent, reproducible, platform-agnostic |

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                     User (Browser)                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Flask Application (app.py)                  │
├──────────────────────────────────────────────────────────┤
│  Routes:                                                 │
│  • /api/chatbot/* ──> Chatbot FSM Engine                │
│  • /api/literacy/* ──> Platform Checklists              │
│  • /health ──────────> Health Check                     │
├──────────────────────────────────────────────────────────┤
│  Logic Layer:                                           │
│  • fsm.py ─────────> Finite State Machine              │
│  • session_manager.py ─> Privacy-preserving sessions   │
├──────────────────────────────────────────────────────────┤
│  Data Layer:                                            │
│  • scenarios.json ─> TFGBV decision trees              │
│  • literacy.json ──> Platform safety guides            │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
digital-shield/                  [31 total files]
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── .dockerignore              # Docker ignore patterns
│
├── routes/                     # API endpoints [4 files]
│   ├── __init__.py
│   ├── chatbot.py             # Chatbot API
│   ├── literacy.py            # Literacy API
│   └── health.py              # Health check
│
├── logic/                      # Business logic [4 files]
│   ├── __init__.py
│   ├── fsm.py                 # Finite State Machine engine
│   ├── scenarios.py           # Scenario definitions
│   └── session_manager.py     # Session handler
│
├── data/                       # JSON data files [2 files]
│   ├── scenarios.json         # Chatbot decision trees
│   └── literacy.json          # Platform checklists
│
├── templates/                  # HTML templates [4 files]
│   ├── base.html              # Base template with CSP
│   ├── index.html             # Landing page
│   ├── chatbot.html           # Chatbot interface
│   └── literacy.html          # Literacy guide
│
├── static/                     # Static assets [7 files]
│   ├── css/
│   │   ├── main.css           # Core styles
│   │   ├── chatbot.css        # Chatbot styles
│   │   └── literacy.css       # Literacy styles
│   ├── js/
│   │   ├── session.js         # Session management
│   │   ├── chatbot.js         # Chatbot logic
│   │   └── literacy.js        # Literacy logic
│   └── images/
│       └── logo.svg           # App logo
│
└── tests/                      # Unit tests [2 files]
    ├── test_fsm.py
    └── test_routes.py
```

**Total:** 31 files | ~174 KB | ~5,000+ lines of code

---

## 🚀 Getting Started

### Prerequisites

- **Docker** (recommended) **OR**
- **Python 3.10+**

### Quick Start (Docker)

```bash
# 1. Clone the repository
git clone https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD.git
cd HACKATHON4-DIGITAL-SHIELD

# 2. Build the image
docker build -t digital-shield .

# 3. Run the container
docker run -d -p 5000:5000 --name digital-shield digital-shield

# 4. Access the application
open http://localhost:5000

# 5. Verify health
curl http://localhost:5000/health
```

### Local Development (Without Docker)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py

# 4. Access the application
open http://localhost:5000
```

---

## 🌐 Deployment Guide

### Method 1: Docker Deployment (Recommended)

#### Production Deployment

```bash
# Build the image
docker build -t digital-shield:latest .

# Run with production settings
docker run -d \
  --name digital-shield \
  -p 5000:5000 \
  --restart unless-stopped \
  -e FLASK_ENV=production \
  digital-shield:latest
```

#### Managing the Container

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

### Method 2: Cloud Deployment

#### Deploy to Render

You can deploy this application to Render with a single click using the button below. This will use the `render.yaml` file in this repository to configure the web service.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD)

Alternatively, you can manually create a new Web Service on [Render.com](https://render.com) and connect your Git repository. Render will automatically detect the `render.yaml` file and configure the service for you.

Key settings from `render.yaml`:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT digital_shield_app:app`
- **Environment:** Python 3.10

#### Deploy to Railway

1. Create a new project on [Railway.app](https://railway.app)
2. Connect your Git repository
3. Railway auto-detects the Dockerfile
4. Deploy automatically

#### Deploy to Fly.io

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

#### Deploy to Heroku

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

### Method 3: VPS Deployment

```bash
# On your VPS (Ubuntu/Debian)
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone and deploy
git clone https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD.git
cd HACKATHON4-DIGITAL-SHIELD
docker build -t digital-shield .
docker run -d -p 80:5000 --restart unless-stopped digital-shield
```

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

## ⚙️ Configuration

### Environment Variables

#### Required
None (app uses secure defaults)

#### Optional

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

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Landing page loads correctly
- [ ] Chatbot scenario selection works
- [ ] Chatbot conversation flows complete successfully
- [ ] Action plans display with all three priority steps
- [ ] Literacy guide platforms load
- [ ] Platform checklists display correctly
- [ ] Session expires after 5 minutes of inactivity
- [ ] Session ends when browser closes
- [ ] Mobile responsive (test at 320px, 375px, 768px)
- [ ] Health check endpoint returns 200

### Automated Testing

```bash
# Run unit tests
python -m pytest tests/

# Test health endpoint
curl http://localhost:5000/health

# Test API endpoints
curl http://localhost:5000/api/chatbot/scenarios
curl http://localhost:5000/api/literacy/platforms
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/
```

---

## 🎨 Design Principles

### Emotional Safety

- **Calming color palette** (blues, purples, soft neutrals)
- **Supportive language** (non-judgmental, anxiety-reducing)
- **Predictable navigation** (no hidden menus, clear paths)
- **Reassuring feedback** (progress indicators, confirmation messages)

### Privacy-by-Design

- **Data minimization** - collect nothing
- **Ephemeral by default** - nothing persists
- **Transparent expiry** - clear session timeout warnings
- **User control** - explicit "End Session" button

### Mobile-First UX

- **320px minimum** screen width support
- **Large touch targets** (44px minimum)
- **Fast loading** on 3G networks
- **Minimal animations** (predictable, smooth)
- **High readability** (16px+ font sizes)

### Target Lighthouse Scores

- **Performance:** >90
- **Accessibility:** >90
- **Best Practices:** >90
- **SEO:** >90

---

## 🔒 Security & Privacy

### Application Security

- **Content Security Policy (CSP)** headers
- **X-Frame-Options: DENY** (clickjacking protection)
- **X-Content-Type-Options: nosniff**
- **Referrer-Policy: no-referrer**
- **Input sanitization** on all user inputs
- **HTTPS-only cookies** in production
- **HTTPOnly cookies** (no JavaScript access)
- **SameSite cookies** (CSRF protection)

### Privacy Features

- **No analytics** tracking
- **No logging** of conversations
- **No persistent** storage
- **Auto-expiry** sessions (5 minutes)
- **No third-party** scripts or fonts

### Production Security Checklist

- ✅ Generate a strong SECRET_KEY
- ✅ Enable HTTPS (use reverse proxy like Nginx)
- ✅ Set FLASK_ENV=production
- ✅ Keep dependencies updated
- ✅ Monitor logs for suspicious activity
- ✅ Use firewall rules to restrict access if needed

---

## 📊 Performance

### Optimization Techniques

- No external JavaScript libraries
- Minified CSS (production)
- Compressed images
- Efficient JSON caching
- Gzip/Brotli compression
- Lazy loading where appropriate

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

### Horizontal Scaling

Deploy multiple instances behind a load balancer:

```bash
# Start multiple containers
docker run -d --name digital-shield-1 -p 5001:5000 digital-shield:latest
docker run -d --name digital-shield-2 -p 5002:5000 digital-shield:latest
docker run -d --name digital-shield-3 -p 5003:5000 digital-shield:latest
```

**Load Balancer (Nginx):**
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

## 🌍 Localization

The application is designed for easy localization.

### JSON Structure

All user-facing content is in JSON files:
- `data/scenarios.json` - Chatbot content
- `data/literacy.json` - Platform guides

### Adding a New Language

1. Create language-specific JSON files:
   - `data/scenarios_sw.json` (Swahili)
   - `data/literacy_sw.json`
2. Update loader to detect language preference
3. Serve appropriate JSON based on language

### Supported Languages

- ✅ **English** (default)
- 🚧 **Swahili** (planned)
- 🚧 **French** (planned)
- 🚧 **Arabic** (planned)

---

## 📋 File Manifest

### Complete File Verification

**Total Files:** 31 ✅

#### Root Level (5 files)
- `app.py` - Flask application entry point
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `.dockerignore` - Docker ignore patterns

#### routes/ (4 files)
- `routes/__init__.py`
- `routes/chatbot.py` - Chatbot API endpoints
- `routes/literacy.py` - Literacy API endpoints
- `routes/health.py` - Health check endpoint

#### logic/ (4 files)
- `logic/__init__.py`
- `logic/fsm.py` - Finite State Machine engine
- `logic/scenarios.py` - Scenario utilities
- `logic/session_manager.py` - Privacy-first session handler

#### data/ (2 files)
- `data/scenarios.json` - Chatbot decision trees (3 scenarios)
- `data/literacy.json` - Platform checklists (5 platforms)

#### templates/ (4 files)
- `templates/base.html` - Base template with CSP headers
- `templates/index.html` - Landing page
- `templates/chatbot.html` - Chatbot interface
- `templates/literacy.html` - Digital literacy guide

#### static/css/ (3 files)
- `static/css/main.css` - Core application styles
- `static/css/chatbot.css` - Chatbot interface styles
- `static/css/literacy.css` - Literacy guide styles

#### static/js/ (3 files)
- `static/js/session.js` - Client-side session manager
- `static/js/chatbot.js` - Chatbot client logic
- `static/js/literacy.js` - Literacy guide client logic

#### static/images/ (1 file)
- `static/images/logo.svg` - Digital Shield logo

#### tests/ (2 files)
- `tests/test_fsm.py` - FSM unit tests
- `tests/test_routes.py` - API integration tests

#### Documentation (3 files)
- `README.md` - This file
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `COMPLETE_FILE_MANIFEST.md` - Verification checklist

### File Size Breakdown

| Category | Size | Files |
|----------|------|-------|
| Python code | ~25 KB | 13 |
| JSON data | ~45 KB | 2 |
| HTML templates | ~15 KB | 4 |
| CSS stylesheets | ~20 KB | 3 |
| JavaScript | ~15 KB | 3 |
| SVG images | ~2 KB | 1 |
| Configuration | ~2 KB | 2 |
| Documentation | ~50 KB | 3 |
| **TOTAL** | **~174 KB** | **31** |

---

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD.git
cd HACKATHON4-DIGITAL-SHIELD

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py
```

### Code Standards

- **PEP 8** for Python code
- **BEM** naming for CSS
- **Semantic HTML5** elements
- **Vanilla JavaScript** (no frameworks)
- **Comprehensive comments** on all functions

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with detailed description

---

## 📈 Roadmap

### MVP (Current) ✅

- ✅ Emergency triage chatbot (3 scenarios)
- ✅ Digital literacy guide (5 platforms)
- ✅ Privacy-by-design architecture
- ✅ Mobile-first responsive design

### Phase 2 🚧

- [ ] Multi-language support (English, Swahili, French, Arabic)
- [ ] Additional scenarios (doxxing, impersonation)
- [ ] More platforms (Telegram, LinkedIn)
- [ ] Offline Progressive Web App (PWA)
- [ ] SMS-based access for feature phones

### Phase 3 🔮

- [ ] Legal resource database by country
- [ ] Community reporting aggregation (anonymous)
- [ ] Integration with existing GBV helplines
- [ ] AI-powered evidence analysis

---

## 📞 Support Resources

### Kenya

- **FIDA Kenya:** 0800 720 553 (Toll-free)
- **GBV Hotline:** 1195
- **Nairobi Women's Hospital:** 0709 400 500
- **COVAW:** 0734 300 300

### Regional Organizations

- **Pollicy (Uganda):** [pollicy.org](https://pollicy.org)
- **Paradigm Initiative:** [paradigmhq.org](https://paradigmhq.org)

---

## 🙏 Acknowledgments

- **FIDA Kenya** for GBV support resources
- **Pollicy** for digital rights research
- **Coalition on Violence Against Women (COVAW)**
- **African Declaration on Internet Rights**

---

## 👨‍💻 Developer Information

**Developed by:** Eng. Stephen Odhiambo  
**Role:** Kenyan AI Engineer & Software Engineer  
**Project:** Digital Shield MVP - TFGBV Response Tool  
**Purpose:** Hackathon submission addressing TFGBV in African digital spaces  
**Built with:** Privacy-by-design principles and emotional sensitivity

### Contact

1. **GitHub:** [ArchAtitocodes](https://github.com/ArchAtitocodes)

2.  **Project Repository:** [HACKATHON4-DIGITAL-SHIELD] (https://github.com/ArchAtitocodes/HACKATHON4-DIGITAL-SHIELD.git)

3. **LIVE DEMO LINK:**[DIGITAL-SHIELD](https://digital-shield-tfgbv-50sl.bolt.host)

4. **VIEW LIVE PITCH DECK LINK ON CANVA:**[DIGITAL-SHIELD] https://www.canva.com/design/DAG5OI5gn6U/oJ207IsDXplVpiwngNLG5g/edit?utm_content=DAG5OI5gn6U&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


---

## 📜 License

[Specify your license - MIT, Apache 2.0, GPL, etc.]

---

## 🎯 Verification Status

**Project Status:** 🟢 PRODUCTION READY

- ✅ **Files Delivered:** 31/31
- ✅ **Features Implemented:** All core features
- ✅ **Documentation Complete:** Comprehensive
- ✅ **Tests Included:** Unit & Integration
- ✅ **Security Hardened:** CSP, XSS, CSRF protection
- ✅ **Privacy Enforced:** Zero data collection
- ✅ **Accessibility Compliant:** WCAG 2.1 AA
- ✅ **Mobile Optimized:** 320px+ support
- ✅ **Deployment Ready:** Docker & Cloud
- ✅ **Hackathon Submission Ready:** Yes

---

## 🏆 Hackathon Submission Checklist

- [x] Complete working application
- [x] Addresses TFGBV in Africa
- [x] Privacy-by-design implementation
- [x] Mobile-first responsive design
- [x] Production deployment ready
- [x] Comprehensive documentation
- [x] Security hardened
- [x] Accessibility compliant
- [x] Culturally appropriate
- [x] Technically excellent

---

## 💡 Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Use a different port
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
# Verify data directory structure
# data/scenarios.json
# data/literacy.json

# Check in container
docker exec digital-shield cat data/scenarios.json
```

### Session Issues

- Sessions expire after 5 minutes of inactivity (by design)
- No data persists beyond session lifetime (privacy feature)
- Check server logs for unusual activity

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [OWASP Security Best Practices](https://owasp.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**🛡️ Digital Shield - Because everyone deserves to be safe online.**

*Protecting Women and Girls in African Digital Spaces*
