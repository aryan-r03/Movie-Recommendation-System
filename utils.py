"""
Utility functions for the Movie Recommendation System
"""
import pandas as pd


def create_sample_dataset():
    """Create a sample movie dataset for demonstration"""
    print("\n⚠️  Creating sample movie dataset...")
    print("   For better results, provide 'movies.csv' with columns:")
    print("   - title, genres, overview/description, rating, etc.\n")

    movies = {
        'title': [
            'The Shawshank Redemption', 'The Godfather', 'The Dark Knight',
            'Pulp Fiction', 'Forrest Gump', 'Inception', 'The Matrix',
            'Goodfellas', 'The Silence of the Lambs', 'Interstellar',
            'The Green Mile', 'Saving Private Ryan', 'The Prestige',
            'The Departed', 'Gladiator', 'The Lion King', 'Toy Story',
            'Avatar', 'Titanic', 'Jurassic Park'
        ],
        'genres': [
            'Drama', 'Crime Drama', 'Action Thriller', 'Crime Drama',
            'Drama Romance', 'Sci-Fi Thriller', 'Sci-Fi Action',
            'Crime Drama', 'Thriller Horror', 'Sci-Fi Drama',
            'Drama Fantasy', 'War Drama', 'Mystery Thriller',
            'Crime Thriller', 'Action Drama', 'Animation Family',
            'Animation Family', 'Sci-Fi Adventure', 'Romance Drama',
            'Adventure Sci-Fi'
        ],
        'overview': [
            'Two imprisoned men bond over years finding redemption through acts of common decency',
            'The aging patriarch of an organized crime dynasty transfers control to his reluctant son',
            'Batman must accept one of the greatest psychological tests to fight injustice',
            'The lives of two mob hitmen a boxer and a pair of diner bandits intertwine',
            'The presidencies of Kennedy and Johnson unfold through perspective of Alabama man',
            'A thief who steals corporate secrets through dream-sharing technology',
            'A computer hacker learns about the true nature of his reality',
            'The story of Henry Hill and his life in the mob',
            'A young FBI cadet must receive help from an incarcerated cannibal killer',
            'A team of explorers travel through a wormhole in space',
            'The lives of guards on Death Row are affected by one of their charges',
            'Following the Normandy Landings a group of soldiers go behind enemy lines',
            'Two stage magicians engage in competitive one-upmanship',
            'An undercover cop and a mole in the police attempt to identify each other',
            'A former Roman General sets out to exact vengeance against the corrupt emperor',
            'Lion cub prince flees his kingdom only to learn the true meaning of responsibility',
            'A cowboy doll is profoundly threatened when a new spaceman figure supplants him',
            'A paraplegic Marine dispatched to the moon Pandora on a unique mission',
            'A seventeen-year-old aristocrat falls in love with a kind but poor artist',
            'A pragmatic paleontologist visiting a theme park fights to survive'
        ],
        'rating': [9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.7, 8.7, 8.6, 8.6,
                   8.6, 8.6, 8.5, 8.5, 8.5, 8.5, 8.3, 7.8, 7.8, 7.9],
        'year': [1994, 1972, 2008, 1994, 1994, 2010, 1999, 1990, 1991, 2014,
                 1999, 1998, 2006, 2006, 2000, 1994, 1995, 2009, 1997, 1993],
        'director': [
            'Frank Darabont', 'Francis Ford Coppola', 'Christopher Nolan',
            'Quentin Tarantino', 'Robert Zemeckis', 'Christopher Nolan',
            'Wachowski Brothers', 'Martin Scorsese', 'Jonathan Demme',
            'Christopher Nolan', 'Frank Darabont', 'Steven Spielberg',
            'Christopher Nolan', 'Martin Scorsese', 'Ridley Scott',
            'Roger Allers', 'John Lasseter', 'James Cameron',
            'James Cameron', 'Steven Spielberg'
        ]
    }

    return pd.DataFrame(movies)


def find_column(df, possible_names):
    """Find a column in DataFrame by checking multiple possible names"""
    for col in df.columns:
        if col.lower() in [name.lower() for name in possible_names]:
            return col
    return None


def preprocess_dataset(df):
    """Preprocess and standardize the movie dataset"""
    print("\n🔄 Preprocessing movie dataset...")

    # Find title column
    title_col = find_column(df, ['title', 'name', 'movie', 'film'])
    if title_col is None:
        print("❌ Could not find title column")
        return None

    processed_df = pd.DataFrame()
    processed_df['title'] = df[title_col]

    # Map other columns
    genre_col = find_column(df, ['genre', 'genres', 'category'])
    if genre_col:
        processed_df['genres'] = df[genre_col]

    overview_col = find_column(df, ['overview', 'description', 'plot', 'summary'])
    if overview_col:
        processed_df['overview'] = df[overview_col]

    rating_col = find_column(df, ['rating', 'score', 'vote_average', 'imdb_rating'])
    if rating_col:
        processed_df['rating'] = pd.to_numeric(df[rating_col], errors='coerce')

    year_col = find_column(df, ['year', 'release_date', 'date'])
    if year_col:
        processed_df['year'] = df[year_col]

    director_col = find_column(df, ['director', 'directors'])
    if director_col:
        processed_df['director'] = df[director_col]

    # Fill missing columns with defaults
    if 'genres' not in processed_df.columns:
        processed_df['genres'] = 'Unknown'
    if 'overview' not in processed_df.columns:
        processed_df['overview'] = processed_df['title']
    if 'rating' not in processed_df.columns:
        processed_df['rating'] = 7.0
    if 'year' not in processed_df.columns:
        processed_df['year'] = 2000
    if 'director' not in processed_df.columns:
        processed_df['director'] = 'Unknown'

    # Fill NaN values
    processed_df = processed_df.fillna({
        'genres': 'Unknown',
        'overview': '',
        'rating': 7.0,
        'year': 2000,
        'director': 'Unknown'
    })

    print(f"✓ Preprocessed {len(processed_df)} movies")
    return processed_df
