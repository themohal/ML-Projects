import streamlit as st
import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

tfidf = pickle.load(open('SMS-Spam-Detection/vectorizer.pkl','rb'))
model = pickle.load(open('SMS-Spam-Detection/model.pkl','rb'))

def transform_text(text):
  text = text.lower()
  text = nltk.word_tokenize(text)
  new = []
  for i in text:
    if i.isalnum():
      new.append(i)
  text = new.copy() #deepcopy
  new.clear()
  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      new.append(i)
  text = new.copy()
  new.clear()
  for i in text:
    new.append(ps.stem(i))
  return " ".join(new)


st.title('Email/SMS Spam Classifier')

user_input = st.text_area("Enter the message")

if st.button('Predict'):
    if user_input!="":
    #prerprocess text
        transformed_input = transform_text(user_input)
    #vectorize
        vector_input = tfidf.transform([transformed_input])
    #predict
        result = model.predict(vector_input)[0]
    #display
        if result==1:
           st.warning('Its a Spam..!')
        else:
           
           st.success('Not Spam..!') 
           
st.write("Developed By: [Muhammad Farjad Ali Raza](https://www.linkedin.com/in/farjadaliraza/)")
