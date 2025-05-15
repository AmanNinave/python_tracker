from fastapi import FastAPI
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app from src
from src.main import app

# For Vercel serverless function compatibility
def handler(request, context):
    return app(request["body"], request["headers"])