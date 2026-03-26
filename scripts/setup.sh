#!/usr/bin/env bash
set -e
echo "🤖 Setting up Social Media AI Agent..."

# Check Python version
python3 -c "import sys; assert sys.version_info >= (3,9), 'Python 3.9+ required'" \
  && echo "✅ Python version OK"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create required directories
mkdir -p data/responses data/logs data/reports

# Copy .env if not exists
if [ ! -f .env ]; then
  cp .env.example .env
  echo "📝 .env created — please fill in your API keys"
else
  echo "✅ .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo "👉 Next: Edit .env with your API keys, then run: python -m src.agent"
