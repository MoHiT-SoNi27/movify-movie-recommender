import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Load environment variables (Ensure you set this in your system)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Store API key securely

def fetch_poster(movie_id):
    """Fetch movie poster URL from TMDb API."""
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"http://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/150"  # Default placeholder
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/150"

@st.cache_resource
def load_data():
    """Load movie dataset and similarity matrix."""
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

def recommend(movie):
    """Recommend 5 similar movies."""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_poster
    except IndexError:
        st.error("Movie not found! Please select a valid movie.")
        return [], []

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie for recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)  # Display recommendations in a row
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
