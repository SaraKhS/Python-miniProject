import streamlit as st
import pandas as pd

st.title('Youtube comment annalizer')
url=st.text_input("Introduce el link del video: ")
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    url : [1, 2, 3, 4],
    'second column': [10, 20, 30, 40] }))