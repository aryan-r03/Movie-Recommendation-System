"""
Configuration settings for the Movie Recommendation System
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Data paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CSV_FILE = os.path.join(DATA_DIR, 'movies.csv')
MODEL_FILE = os.path.join(DATA_DIR, 'movie_model.pkl')

# Frontend paths
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

# Flask settings
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Recommendation settings
MAX_FEATURES = 5000
DEFAULT_RECOMMENDATIONS = 5
MAX_TOP_RATED = 10

# API settings
CORS_ORIGINS = '*'  # In production, specify exact origins
