import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv() # This reads the environment variables inside .env
api = os.getenv('OPEN_AI_API')

import os
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Image Creation Using OpenAI API")

user_input = st.text_input("Write text to create image:", "")


#print(d['data'][0]['url'])
if st.button("Create Image"):
    if user_input!="":
        response = openai.Image.create(
        prompt=user_input,
        n=1,
        size="512x512"
        )
        st.write(user_input.capitalize())
        st.image(response['data'][0]['url'], width=512, 
         # Manually Adjust the width of the image as per requirement 
        )
    else:
        st.write("Please write something to create image")

    
st.write("Developed By: [Muhammad Farjad Ali Raza](https://www.linkedin.com/in/farjadaliraza/)")
