import numpy as np
import streamlit as st
import pickle
import pandas as pd


model = pickle.load(open('CGPA-IQ-Placement/model.pkl', 'rb'))

st.title("CGPA IQ PLACEMENT")

user_input1 = st.text_input("Enter CGPA :")
user_input2 = st.text_input("Enter IQ :")

def predict(inp1,inp2):
    '''
    For rendering results on HTML GUI
    '''
    init_features = [float(inp1),float(inp2)]
    final_features = [np.array(init_features)]

    return model.predict(final_features) # making prediction
    
        
 
if st.button('Predict'):
    prediction = predict(user_input1,user_input2)
    prediction_text=''
    if prediction >=1:
        prediction_text = "Placement is confirmed"
        st.success(prediction_text)
    else:
        prediction_text = "Placement is not confirmed"
        st.success(prediction_text)
