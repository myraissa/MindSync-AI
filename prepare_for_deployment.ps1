Write-Host "🚀 Preparing for Streamlit Cloud deployment..."

# 1. Create requirements.txt
$requirements = @"
# Core Dependencies for Streamlit Cloud
streamlit==1.30.0
pydantic==2.5.0
python-dotenv==1.0.0

# ML & NLP (only essentials for cloud)
transformers==4.36.0
torch==2.1.0
scikit-learn==1.4.0
sentence-transformers==2.3.0

# Utilities
requests==2.31.0
numpy==1.26.0
pandas==2.1.0
"@

Set-Content -Path "requirements.txt" -Value $requirements -Encoding UTF8
Write-Host "✅ Created lightweight requirements.txt"

# 2. Create .streamlit directory
if (!(Test-Path ".streamlit")) {
   New-Item -ItemType Directory -Path ".streamlit" | Out-Null
}

# 3. Create Streamlit config
$config = @"
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
"@

Set-Content -Path ".streamlit/config.toml" -Value $config -Encoding UTF8
Write-Host "✅ Created Streamlit config"

# 4. Create secrets template
$secrets = @"
# Streamlit Secrets Configuration
# Copy this to .streamlit/secrets.toml and fill in your values
# DO NOT commit secrets.toml to Git!

HUGGINGFACE_TOKEN = "your_token_here"
ENVIRONMENT = "production"
"@

Set-Content -Path ".streamlit/secrets.toml.example" -Value $secrets -Encoding UTF8
Write-Host "✅ Created secrets template"

# 5. Create .gitignore
$gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Streamlit
.streamlit/secrets.toml

# Data & Models
data/
models/
*.pkl
*.pth
*.h5

# Logs
logs/
*.log

# Environment
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"@

Set-Content -Path ".gitignore" -Value $gitignore -Encoding UTF8
Write-Host "✅ Created/updated .gitignore"

# 6. Create deployment README
$readme = @"
# 🚀 Deployment Instructions

## Streamlit Cloud Deployment

### Steps
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Select repo and set:
   app/streamlit_app.py
4. Add secrets in dashboard
5. Deploy 🚀
"@

Set-Content -Path "DEPLOYMENT_README.md" -Value $readme -Encoding UTF8
Write-Host "✅ Created deployment README"

Write-Host ""
Write-Host "=========================================="
Write-Host "✅ Deployment preparation complete!"
Write-Host "=========================================="
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Fill in .streamlit/secrets.toml"
Write-Host "2. Test locally: streamlit run app/streamlit_app.py"
Write-Host "3. Push to GitHub"
Write-Host "4. Deploy on Streamlit Cloud"
