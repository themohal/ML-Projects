import streamlit as st
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import pandas as pd


# Load the model and tokenizer
model = load_model("html_correction_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# df.to_csv('Html_Code_Correction_Dataset.csv',index=False)
df = pd.read_csv("Html_Code_Correction_Dataset.csv")
bad_practices = df["Bad_Practices"]
good_practices = df["Good_Practices"]

# Convert texts to sequences and pad them for consistent length
X_bad = tokenizer.texts_to_sequences(bad_practices)
X_good = tokenizer.texts_to_sequences(good_practices)
X = pad_sequences(X_bad + X_good, padding="post")

# Label bad as 0 and good as 1
y_bad = [0] * len(X_bad)
y_good = [1] * len(X_good)
y = np.array(y_bad + y_good)


def rectify_html(html_code):
    # For simplicity, we use a rule-based approach to fix the bad practices
    rectifications = {
        "<p>This is bad": "<p>This is good</p>",
        "<center>Centered content": "<div style='text-align: center;'>Centered content</div>",
        "<div style='color: red'>": "<div><span style='color: red'>Red text</span></div>",
        "<table><tr><td>Layout</td></tr></table>": "<div>Layout with CSS</div>",
        "<img src='image.jpg'>": "<img src='image.jpg' alt='Image description'>",
        "This is content": "<div>This is content</div>",
        "<div custom-attr='value'>": "<div data-custom-attr='value'>",
        "<div id='duplicateID'>": "<div id='uniqueID'>",
        "<img src='http://insecure.com/image.jpg'>": "<img src='https://secure.com/image.jpg'>",
        "<div>This is div</div>": "<section>This is section</section>",
    }
    # Replace any matching bad practice in the provided code
    for bad, good in rectifications.items():
        html_code = html_code.replace(bad, good)
    return html_code


def predict_and_rectify(html_code):
    # Convert the html_code to a sequence and pad it
    sequence = tokenizer.texts_to_sequences([html_code])
    padded_sequence = pad_sequences(sequence, maxlen=X.shape[1], padding="post")

    # Predict
    prediction = model.predict(padded_sequence)

    # If it's bad practice (prediction close to 0), rectify it
    if prediction[0][0] < 0.5:
        corrected_html = rectify_html(html_code)
        return "Bad Practice. Rectified Code:", corrected_html
    else:
        return "Good Practice."


st.title("HTML Auto-Correct Tool")

user_input = st.text_area("Paste your HTML code:")

if user_input:
    corrected_code = predict_and_rectify(user_input)  # or use your prediction function
    st.text_area("Corrected Code:", value=corrected_code, height=200)
