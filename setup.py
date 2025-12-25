"""Setup configuration for Strava Race Time Predictor"""
from setuptools import setup, find_packages

setup(
    name="strava-predictor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "joblib>=1.1.0",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
)
