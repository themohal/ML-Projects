import streamlit as st
from PIL import Image
import io
import numpy as np
from tensorflow import keras
st.title('Cat Vs Dog Classification')

#adding a file uploader
class_names = ['Cat','Dog']
model = keras.models.load_model('Cats-vs-Dogs/model.h5')

file = st.file_uploader("Please choose a file")

if file is not None:

    #To read file as bytes:

    bytes_data = file.getvalue()
    
    image = Image.open(io.BytesIO(bytes_data))
    newsize = (256, 256)
    image_new = image.resize(newsize)
    image = image_new.convert('RGB')
    image = np.array(image)
    test_input = image.reshape((1,256,256,3))
    
    
    result = int(model.predict(test_input)[0][0])
    st.success("Predicted Class is : "+class_names[result])
    st.image(image_new)

st.write("Developed By: [Muhammad Farjad Ali Raza](https://www.linkedin.com/in/farjadaliraza/)")

