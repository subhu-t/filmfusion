import streamlit as st
import pickle
import pandas as pd
import  requests
def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a886a3ce6c9a8b4543c44c2f2b0cc4a1'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]
    rm=[]
    rmp=[]
    for i in movies_list:
        movie_id=moviess.iloc[i[0]].movie_id

        rm.append(movies.iloc[i[0]].title)
        # fetch poster using api
        rmp.append(fetch_poster(movie_id))
    return rm,rmp


movies_list=pickle.load(open('movies.pkl','rb'))
movies_list=movies_list['title'].values

movies_id=pickle.load(open('movies.pkl','rb'))
movies_id=movies_id['movie_id'].values

movies = pd.DataFrame(movies_list, columns=['title'])
moviess=pd.DataFrame(movies_id, columns=['movie_id'])

similarity=pickle.load(open('similarity.pkl','rb'))


st.title('FilmFusion')

smn = st.selectbox(
'Enter Movie Name',movies_list)

if st.button('show'):
    names,posters=recommend(smn)
    num_columns = 3  # Number of columns
    num_rows = (len(names) + num_columns - 1) // num_columns  # Calculate the number of rows

    cols = st.columns(num_columns)

    for i in range(num_rows):
        for j in range(num_columns):
            index = i * num_columns + j
            if index < len(names):
                with cols[j]:
                    st.header(names[index])
                    st.image(posters[index])