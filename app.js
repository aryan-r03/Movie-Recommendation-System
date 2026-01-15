// Movie Recommendation System - Frontend JavaScript

// API Configuration
const API_BASE = window.location.origin;

// DOM Elements
const movieInput = document.getElementById('movieInput');
const recommendBtn = document.getElementById('recommendBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const topMoviesContainer = document.getElementById('topMovies');
const totalMoviesEl = document.getElementById('totalMovies');
const recommendationsGrid = document.getElementById('recommendationsGrid');

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeStars();
    loadStats();
    loadTopMovies();
    setupEventListeners();
});

// Create animated stars background
function initializeStars() {
    const starsContainer = document.getElementById('stars');
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        starsContainer.appendChild(star);
    }
}

// Setup event listeners
function setupEventListeners() {
    recommendBtn.addEventListener('click', getRecommendations);
    movieInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            getRecommendations();
        }
    });
}

// Load system statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        const data = await response.json();
        
        if (data.success) {
            totalMoviesEl.textContent = data.total_movies;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        totalMoviesEl.textContent = 'N/A';
    }
}

// Load top rated movies
async function loadTopMovies() {
    try {
        const response = await fetch(`${API_BASE}/api/top-rated?n=5`);
        const data = await response.json();
        
        if (data.success && data.movies) {
            displayTopMovies(data.movies);
        }
    } catch (error) {
        console.error('Error loading top movies:', error);
    }
}

// Display top rated movies in sidebar
function displayTopMovies(movies) {
    topMoviesContainer.innerHTML = '';
    
    movies.forEach(movie => {
        const movieItem = document.createElement('div');
        movieItem.className = 'movie-item';
        movieItem.innerHTML = `
            <div class="movie-title">${escapeHtml(movie.title)}</div>
            <div class="movie-meta">
                <span class="movie-rating">★ ${movie.rating}</span>
                ${escapeHtml(movie.genres)} • ${movie.year}
            </div>
        `;
        
        movieItem.addEventListener('click', () => {
            movieInput.value = movie.title;
            getRecommendations();
        });
        
        topMoviesContainer.appendChild(movieItem);
    });
}

// Get movie recommendations
async function getRecommendations() {
    const title = movieInput.value.trim();
    
    if (!title) {
        showError('⚠️ Please enter a movie title');
        return;
    }
    
    // Show loading state
    recommendBtn.disabled = true;
    loading.classList.add('show');
    resultsSection.classList.remove('show');
    
    try {
        const response = await fetch(`${API_BASE}/api/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                n: 6
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.result);
        } else {
            showError('❌ ' + (data.error || 'Movie not found in database'));
        }
    } catch (error) {
        console.error('Error:', error);
        showError('❌ Failed to get recommendations. Please try again.');
    } finally {
        recommendBtn.disabled = false;
        loading.classList.remove('show');
    }
}

// Display recommendation results
function displayResults(result) {
    // Display query movie information
    const queryMovie = result.query_movie;
    document.getElementById('queryTitle').textContent = queryMovie.title;
    document.getElementById('queryRating').textContent = '★ ' + queryMovie.rating;
    document.getElementById('queryGenres').textContent = queryMovie.genres;
    document.getElementById('queryYear').textContent = queryMovie.year;
    document.getElementById('queryOverview').textContent = queryMovie.overview;
    
    // Display recommendations
    recommendationsGrid.innerHTML = '';
    
    result.recommendations.forEach((movie, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.style.animationDelay = `${index * 0.1}s`;
        
        card.innerHTML = `
            <div class="rec-title">${escapeHtml(movie.title)}</div>
            <div class="rec-genres">${escapeHtml(movie.genres)}</div>
            <div class="rec-meta">
                <span>★ ${movie.rating}</span>
                <span>${movie.year}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <span class="similarity-badge">${movie.similarity}% Match</span>
            </div>
            <div class="rec-overview">${escapeHtml(movie.overview)}</div>
        `;
        
        card.addEventListener('click', () => {
            movieInput.value = movie.title;
            getRecommendations();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        recommendationsGrid.appendChild(card);
    });
    
    // Show results section
    resultsSection.classList.add('show');
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }, 100);
}

// Show error message
function showError(message) {
    alert(message);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Search movies (optional feature)
async function searchMovies(query) {
    try {
        const response = await fetch(`${API_BASE}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.results;
        }
        return [];
    } catch (error) {
        console.error('Search error:', error);
        return [];
    }
}