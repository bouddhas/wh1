import streamlit as st
import pandas as pd
import numpy as np

st.title('OC credit default project')
st.write("Hello from Streamlit")

@st.cache
def load_data(nrows):
    data = pd.read_csv('data.csv', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
    # Create a text element and let the reader know the data is loading.
    data_load_state.text("Done! (using st.cache)")
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')

st.subheader('retest')
hist_values = np.histogram(
    data[FLAG_OWN_CAR].dt, bins=2, range=(0,1))[0]
st.bar_chart(hist_values)

