#!/bin/bash

echo "======================================================================"
echo "Strava Race Time Predictor - Setup Script"
echo "======================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create directories
echo ""
echo "Creating project directories..."
mkdir -p data models plots

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Strava API credentials"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "======================================================================"
echo "Setup Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Strava credentials"
echo "   - Go to https://www.strava.com/settings/api"
echo "   - Create an application and get your Client ID and Client Secret"
echo ""
echo "2. Get your refresh token:"
echo "   python strava_auth.py"
echo ""
echo "3. Run the quick start:"
echo "   python quickstart.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "   source venv/bin/activate"
echo ""
