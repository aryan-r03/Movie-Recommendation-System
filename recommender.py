"""
Movie Recommendation Engine using Content-Based Filtering
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MinMaxScaler
import pickle
import os
import warnings

from config import MAX_FEATURES, CSV_FILE, MODEL_FILE
from utils import create_sample_dataset, preprocess_dataset

warnings.filterwarnings('ignore')


class MovieRecommendationSystem:
    def __init__(self):
        self.movies_df = None
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=MAX_FEATURES)
        self.cosine_sim = None
        self.indices = None
        self.scaler = MinMaxScaler()

    def load_movies_dataset(self, csv_path=None):
        """Load movie dataset from CSV file"""
        if csv_path is None:
            csv_path = CSV_FILE

        try:
            if os.path.exists(csv_path):
                print(f"\n📥 Loading dataset from {csv_path}...")
                df = pd.read_csv(csv_path)
                print(f"✓ Loaded {len(df)} movies")
                print(f"✓ Columns: {df.columns.tolist()}")
                print(f"\n📊 Sample data:")
                print(df.head())
                return df
            else:
                print(f"✗ File '{csv_path}' not found")
                return create_sample_dataset()
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            return create_sample_dataset()

    def build_recommendation_engine(self, df):
        """Build the recommendation engine from dataset"""
        print("\n" + "=" * 70)
        print("BUILDING MOVIE RECOMMENDATION ENGINE")
        print("=" * 70)

        # Preprocess dataset
        self.movies_df = preprocess_dataset(df)
        if self.movies_df is None:
            return False

        # Create combined features
        print("\n🔍 Creating feature matrix...")
        self.movies_df['combined_features'] = (
            self.movies_df['genres'].fillna('') + ' ' +
            self.movies_df['overview'].fillna('') + ' ' +
            self.movies_df['director'].fillna('')
        )

        # Compute TF-IDF vectors
        print("🔢 Computing TF-IDF vectors...")
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movies_df['combined_features']
        )

        # Compute cosine similarity
        print("📊 Computing similarity matrix...")
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Create indices mapping
        self.indices = pd.Series(
            self.movies_df.index,
            index=self.movies_df['title']
        ).drop_duplicates()

        print("\n" + "=" * 70)
        print(f"✅ RECOMMENDATION ENGINE READY")
        print(f"   Total Movies: {len(self.movies_df)}")
        print(f"   Features: {tfidf_matrix.shape[1]}")
        print("=" * 70)

        return True

    def get_recommendations(self, title, n=5):
        """Get movie recommendations based on a given title"""
        try:
            # Find movie by partial match
            title_lower = title.lower()
            matches = self.movies_df[
                self.movies_df['title'].str.lower().str.contains(title_lower, na=False)
            ]

            if len(matches) == 0:
                return {'error': f'Movie "{title}" not found in database'}

            # Get exact title and index
            exact_title = matches.iloc[0]['title']
            idx = self.indices[exact_title]

            # Get similarity scores
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:n + 1]  # Exclude the movie itself

            movie_indices = [i[0] for i in sim_scores]

            # Build recommendations list
            recommendations = []
            for i, movie_idx in enumerate(movie_indices):
                movie = self.movies_df.iloc[movie_idx]
                overview = str(movie['overview'])
                recommendations.append({
                    'title': movie['title'],
                    'genres': movie['genres'],
                    'rating': float(movie['rating']),
                    'year': int(movie['year']) if pd.notna(movie['year']) else 2000,
                    'similarity': round(sim_scores[i][1] * 100, 2),
                    'overview': overview[:200] + '...' if len(overview) > 200 else overview
                })

            # Get original movie info
            original_movie = self.movies_df.iloc[idx]

            return {
                'query_movie': {
                    'title': original_movie['title'],
                    'genres': original_movie['genres'],
                    'rating': float(original_movie['rating']),
                    'year': int(original_movie['year']) if pd.notna(original_movie['year']) else 2000,
                    'overview': original_movie['overview']
                },
                'recommendations': recommendations,
                'total_movies': len(self.movies_df)
            }

        except Exception as e:
            print(f"❌ Recommendation error: {e}")
            return {'error': str(e)}

    def get_top_rated_movies(self, n=10):
        """Get top rated movies"""
        try:
            top_movies = self.movies_df.nlargest(n, 'rating')
            results = []

            for _, movie in top_movies.iterrows():
                overview = str(movie['overview'])
                results.append({
                    'title': movie['title'],
                    'genres': movie['genres'],
                    'rating': float(movie['rating']),
                    'year': int(movie['year']) if pd.notna(movie['year']) else 2000,
                    'overview': overview[:150] + '...' if len(overview) > 150 else overview
                })

            return results
        except Exception as e:
            print(f"Error getting top rated: {e}")
            return []

    def search_movies(self, query):
        """Search movies by title or genre"""
        try:
            query_lower = query.lower()
            matches = self.movies_df[
                (self.movies_df['title'].str.lower().str.contains(query_lower, na=False)) |
                (self.movies_df['genres'].str.lower().str.contains(query_lower, na=False))
            ]

            results = []
            for _, movie in matches.head(10).iterrows():
                results.append({
                    'title': movie['title'],
                    'genres': movie['genres'],
                    'rating': float(movie['rating']),
                    'year': int(movie['year']) if pd.notna(movie['year']) else 2000
                })

            return results
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def save_model(self, filepath=None):
        """Save the trained model to disk"""
        if filepath is None:
            filepath = MODEL_FILE

        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'movies_df': self.movies_df,
                    'tfidf_vectorizer': self.tfidf_vectorizer,
                    'cosine_sim': self.cosine_sim,
                    'indices': self.indices
                }, f)
            print(f"\n✓ Model saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

    def load_model(self, filepath=None):
        """Load a pre-trained model from disk"""
        if filepath is None:
            filepath = MODEL_FILE

        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.movies_df = data['movies_df']
                self.tfidf_vectorizer = data['tfidf_vectorizer']
                self.cosine_sim = data['cosine_sim']
                self.indices = data['indices']
            print(f"✓ Model loaded from {filepath}")
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
