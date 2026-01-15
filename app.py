"""
Flask Application - Movie Recommendation System API
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from recommender import MovieRecommendationSystem
from config import (
    FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
    FRONTEND_DIR, MODEL_FILE, CSV_FILE,
    CORS_ORIGINS, DEFAULT_RECOMMENDATIONS, MAX_TOP_RATED
)

# Initialize Flask app
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app, origins=CORS_ORIGINS)

# Initialize recommendation system
recommender = MovieRecommendationSystem()


def initialize_system():
    """Initialize or load the recommendation system"""
    print("\n" + "=" * 70)
    print("INITIALIZING MOVIE RECOMMENDATION SYSTEM")
    print("=" * 70)

    # Try to load existing model
    if recommender.load_model(MODEL_FILE):
        print("✓ Using pre-trained model (delete to rebuild)")
        return True

    # Build new model
    print("\nNo existing model found. Building new model...")
    df = recommender.load_movies_dataset(CSV_FILE)

    if recommender.build_recommendation_engine(df):
        recommender.save_model(MODEL_FILE)
        return True
    else:
        print("❌ Failed to build recommendation engine")
        return False


# Initialize on startup
initialize_system()


# ==================== ROUTES ====================

@app.route('/')
def home():
    """Serve the main HTML page"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory(FRONTEND_DIR, path)


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Get movie recommendations"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        n = data.get('n', DEFAULT_RECOMMENDATIONS)

        if not title:
            return jsonify({
                'success': False,
                'error': 'No title provided'
            }), 400

        result = recommender.get_recommendations(title, n)

        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/top-rated', methods=['GET'])
def top_rated():
    """Get top rated movies"""
    try:
        n = int(request.args.get('n', MAX_TOP_RATED))
        movies = recommender.get_top_rated_movies(n)

        return jsonify({
            'success': True,
            'movies': movies
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
def search():
    """Search movies by title or genre"""
    try:
        data = request.get_json()
        query = data.get('query', '')

        if not query:
            return jsonify({
                'success': False,
                'error': 'No query provided'
            }), 400

        results = recommender.search_movies(query)

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get system statistics"""
    try:
        total = len(recommender.movies_df) if recommender.movies_df is not None else 0

        return jsonify({
            'success': True,
            'total_movies': total,
            'algorithm': 'Content-Based Filtering',
            'similarity_metric': 'Cosine Similarity'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'total_movies': 0,
            'error': str(e)
        })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Movie Recommendation API'
    })


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("STARTING FLASK SERVER")
    print("=" * 70)
    print(f"\n📌 Installation:")
    print(f"   pip install flask flask-cors pandas numpy scikit-learn")
    print(f"\n📄 Dataset:")
    print(f"   Place 'movies.csv' in the 'data/' folder")
    print(f"\n🌐 Server running on: http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"   Access locally: http://127.0.0.1:{FLASK_PORT}")
    print("\n" + "=" * 70 + "\n")

    app.run(debug=FLASK_DEBUG, port=FLASK_PORT, host=FLASK_HOST)
