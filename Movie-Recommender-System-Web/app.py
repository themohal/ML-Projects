import streamlit as st
import pickle
import pandas as pd
import requests
import shutil
shutil.unpack_archive('Movie-Recommender-System-Web/Movie-Recommender-System-Web.zip', 'Movie-Recommender-System-Web')

movies = pickle.load(open('Movie-Recommender-System-Web/movies.pkl','rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('Movie-Recommender-System-Web/similarity.pkl','rb'))

#print(movies_list['title'].values)
st.title("Movies Recommender System")
selected_movies_name = st.selectbox(
    'Select Movies To Check?',
    (sorted(movies['title'].values)))
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=3d1bcceb8448d173819c3d2d33acc4ab&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w780"+str(data['poster_path'])

def recommend(movie):
    movie_index = movies[movies['title'] == movie ].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
         #fetching poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommended,recommend_movies_poster
    

if st.button('Recommend'):
    movie_name,posters = recommend(selected_movies_name)
    #print(posters)
    col1, col2, col3,col4, col5 = st.columns(5)

    with col1:
        st.text(movie_name[0])
        st.image(posters[0])

    with col2:
        st.text(movie_name[1])
        st.image(posters[1])

    with col3:
        st.text(movie_name[2])
        st.image(posters[2])
    with col4:
        st.text(movie_name[3])
        st.image(posters[3])
    with col5:
        st.text(movie_name[4])
        st.image(posters[4])
    #for i in movie_name:
    #   st.write(i)


