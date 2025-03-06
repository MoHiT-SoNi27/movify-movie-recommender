import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2aa43989b26970e2f21b63120532180c&language=en-US")
    data = response.json()

    if 'poster_path' not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500"  # Placeholder image if poster is missing

    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  # Get correct movie ID
        recommended_movies.append(movies.iloc[i[0]].title)  # Use correct index
        recommended_movies_poster.append(fetch_poster(movie_id))  # Fetch poster
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, poster = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns in a row

    for i in range(5):
        with cols[i]:  # Assign each movie to a different column
            st.text(names[i])
            st.image(poster[i])

