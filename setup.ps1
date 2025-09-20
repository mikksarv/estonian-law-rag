# setup.ps1

# Move to project root (optional, just to be safe)
cd E:\EST_LAW_RAG\estonian-law-rag

# Create virtual environment if it doesn't exist
if (-Not (Test-Path ".\venv")) {
    python -m venv venv
}

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

Write-Output "✅ Setup complete. You can now run your scripts."