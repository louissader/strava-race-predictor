#!/bin/bash

# Script to upload Strava Race Predictor to GitHub

echo "======================================================================"
echo "  Upload Strava Race Predictor to GitHub"
echo "======================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Not in the project directory"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git initialized"
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo "❌ .gitignore not found!"
    exit 1
fi

echo ""
echo "Before we continue, you need to:"
echo "1. Go to https://github.com/new"
echo "2. Create a new repository (e.g., 'strava-race-predictor')"
echo "3. Don't initialize with README, .gitignore, or license"
echo ""
read -p "Have you created the GitHub repository? (y/n): " created

if [ "$created" != "y" ]; then
    echo "Please create the repository first, then run this script again."
    exit 0
fi

echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ No repository URL provided"
    exit 1
fi

echo ""
echo "======================================================================"
echo "  Preparing files for upload..."
echo "======================================================================"
echo ""

# Add all files
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Strava Race Time Predictor ML project

- Fetches all activities from Strava API with pagination
- Trains ML models (Random Forest, Gradient Boosting, Ridge, Lasso)
- Predicts race times for 5K, 10K, Half Marathon, Marathon
- Comprehensive training analysis and visualizations
- Easy-to-use interface with multiple entry points
- Complete documentation and setup guides"

echo "✅ Commit created"

# Add remote
echo ""
echo "Adding GitHub remote..."
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
echo "✅ Remote added"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "  ✅ SUCCESS! Project uploaded to GitHub"
    echo "======================================================================"
    echo ""
    echo "Your project is now at: $repo_url"
    echo ""
    echo "Next steps:"
    echo "1. Visit your repository on GitHub"
    echo "2. Add a description and topics (machine-learning, strava, python, etc.)"
    echo "3. Share with others!"
    echo ""
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "1. Check your GitHub credentials"
    echo "2. Make sure the repository exists"
    echo "3. Try: git push -u origin main --force (if you're sure)"
fi
