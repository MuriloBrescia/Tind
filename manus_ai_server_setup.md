# Manus AI Server Setup & Deployment Guide

## 🚀 Quick Start Prompt for Manus AI Server

### Prerequisites Check
```bash
# Check system requirements
python3 --version  # Python 3.8+ required
node --version     # Node.js 16+ required
docker --version   # Docker (optional but recommended)
git --version      # Git for cloning repositories
```

### 1. Environment Setup
```bash
# Create project directory
mkdir manus-ai-server && cd manus-ai-server

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Update pip
pip install --upgrade pip
```

### 2. Manus AI Installation Options

#### Option A: From GitHub Repository
```bash
# Clone Manus AI repository
git clone https://github.com/manus-ai/manus-core.git
cd manus-core

# Install dependencies
pip install -r requirements.txt
npm install  # If frontend components exist
```

#### Option B: PyPI Installation
```bash
# Install via pip
pip install manus-ai

# Or with specific extras
pip install manus-ai[server,gpu,all]
```

#### Option C: Docker Deployment
```bash
# Pull official Manus AI image
docker pull manusai/manus-server:latest

# Run with docker-compose
curl -o docker-compose.yml https://raw.githubusercontent.com/manus-ai/manus-core/main/docker-compose.yml
docker-compose up -d
```

### 3. Configuration Setup

#### Create Configuration File
```bash
# Create config directory
mkdir -p config

# Generate default config
cat > config/manus_config.yaml << EOF
server:
  host: "0.0.0.0"
  port: 8080
  debug: false
  workers: 4

ai_models:
  default_model: "gpt-3.5-turbo"
  model_cache_dir: "./models"
  max_tokens: 4096
  temperature: 0.7

database:
  type: "sqlite"  # or postgresql, mysql
  url: "sqlite:///manus.db"
  
storage:
  type: "local"  # or s3, gcs
  path: "./data"

security:
  secret_key: "your-secret-key-here"
  api_key_required: true
  cors_enabled: true
  
logging:
  level: "INFO"
  file: "./logs/manus.log"
EOF
```

#### Environment Variables
```bash
# Create .env file
cat > .env << EOF
MANUS_CONFIG_PATH=./config/manus_config.yaml
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
HUGGINGFACE_TOKEN=your_hf_token_here

# Database (if using external DB)
DATABASE_URL=postgresql://user:pass@localhost:5432/manus

# Storage (if using cloud storage)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=your_bucket_name

# Server specific
MANUS_HOST=0.0.0.0
MANUS_PORT=8080
MANUS_WORKERS=4
EOF
```

### 4. Database Setup
```bash
# Initialize database
manus db init

# Run migrations
manus db migrate

# Create admin user (optional)
manus user create-admin --email admin@example.com --password admin123
```

### 5. Start Manus AI Server

#### Development Mode
```bash
# Start with development server
manus serve --host 0.0.0.0 --port 8080 --debug

# Or using Python directly
python -m manus.server --config config/manus_config.yaml
```

#### Production Mode
```bash
# Using Gunicorn (recommended for production)
gunicorn manus.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 300

# Using Uvicorn (ASGI server)
uvicorn manus.asgi:application \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 4

# Background service
nohup manus serve --config config/manus_config.yaml > manus.log 2>&1 &
```

#### Docker Production
```bash
# Build custom image
docker build -t manus-ai-custom .

# Run with custom config
docker run -d \
    --name manus-ai-server \
    -p 8080:8080 \
    -v $(pwd)/config:/app/config \
    -v $(pwd)/data:/app/data \
    --env-file .env \
    manus-ai-custom
```

### 6. Server Access & Testing

#### Health Check
```bash
# Check if server is running
curl http://localhost:8080/health

# Check API status
curl http://localhost:8080/api/v1/status

# Test AI endpoint
curl -X POST http://localhost:8080/api/v1/chat \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -d '{"message": "Hello, Manus AI!", "model": "gpt-3.5-turbo"}'
```

#### Web Interface Access
```bash
# Open in browser
http://localhost:8080
http://your-server-ip:8080

# For mobile access
http://your-public-ip:8080
```

### 7. Network Configuration

#### Firewall Rules
```bash
# Ubuntu/Debian
sudo ufw allow 8080/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

#### Nginx Reverse Proxy (Optional)
```bash
# Install Nginx
sudo apt install nginx

# Create config
sudo tee /etc/nginx/sites-available/manus-ai << EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/manus-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Monitoring & Logs

#### View Logs
```bash
# Real-time logs
tail -f logs/manus.log

# Docker logs
docker logs -f manus-ai-server

# System service logs
sudo journalctl -u manus-ai -f
```

#### Performance Monitoring
```bash
# Check resource usage
htop
docker stats  # For containerized deployment

# Monitor API calls
curl http://localhost:8080/api/v1/metrics
```

### 9. Troubleshooting

#### Common Issues & Solutions
```bash
# Port already in use
sudo lsof -i :8080
sudo kill -9 <PID>

# Permission issues
sudo chown -R $USER:$USER ./data ./logs
chmod 755 ./data ./logs

# Memory issues
# Reduce workers in config
# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Model loading issues
# Check model cache
ls -la ./models/
# Clear cache and re-download
rm -rf ./models/* && manus models download
```

### 10. API Usage Examples

#### Python Client
```python
import requests

# API endpoint
api_url = "http://your-server:8080/api/v1"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

# Chat completion
response = requests.post(
    f"{api_url}/chat",
    headers=headers,
    json={
        "message": "Explain quantum computing",
        "model": "gpt-4",
        "temperature": 0.7
    }
)
print(response.json())

# File upload
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{api_url}/upload", headers=headers, files=files)
```

#### JavaScript Client
```javascript
// Browser/Node.js
const response = await fetch('http://your-server:8080/api/v1/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
        message: 'Hello Manus AI!',
        model: 'gpt-3.5-turbo'
    })
});

const result = await response.json();
console.log(result);
```

### 11. Scaling & Production

#### Load Balancer Setup
```bash
# HAProxy configuration
sudo apt install haproxy

sudo tee -a /etc/haproxy/haproxy.cfg << EOF
frontend manus_frontend
    bind *:80
    default_backend manus_servers

backend manus_servers
    balance roundrobin
    server manus1 127.0.0.1:8080 check
    server manus2 127.0.0.1:8081 check
    server manus3 127.0.0.1:8082 check
EOF

sudo systemctl restart haproxy
```

#### Auto-restart Service
```bash
# Create systemd service
sudo tee /etc/systemd/system/manus-ai.service << EOF
[Unit]
Description=Manus AI Server
After=network.target

[Service]
Type=exec
User=ubuntu
WorkingDirectory=/home/ubuntu/manus-ai-server
Environment=PATH=/home/ubuntu/manus-ai-server/venv/bin
ExecStart=/home/ubuntu/manus-ai-server/venv/bin/manus serve --config config/manus_config.yaml
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable manus-ai
sudo systemctl start manus-ai
sudo systemctl status manus-ai
```

## 🔐 Security Checklist
- [ ] Change default passwords/API keys
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular backups of data/config
- [ ] Update dependencies regularly

## 📚 Additional Resources
- Official Documentation: https://docs.manus-ai.com
- GitHub Repository: https://github.com/manus-ai/manus-core
- Discord Community: https://discord.gg/manus-ai
- API Reference: https://api.manus-ai.com/docs

---
**Note:** Replace placeholder values (API keys, domains, IPs) with your actual values.