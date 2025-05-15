import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app from src
from src.main import app

# This is the correct syntax for Vercel - nothing more is needed
app = app