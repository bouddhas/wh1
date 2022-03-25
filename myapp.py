import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt

st.title('OC credit default project')
st.write("Hello from Streamlit")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.write(df)

  # Add some matplotlib code !
  fig, ax = plt.subplots()
  df.hist(
    bins=8,
    column="Age",
    grid=False,
    figsize=(8, 8),
    color="#86bf91",
    zorder=2,
    rwidth=0.9,
    ax=ax,)
  st.write(fig)



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
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('retest')
hist_values = np.histogram(
    data[FLAG_OWN_CAR].dt, bins=2, range=(0,1))[0]
st.bar_chart(hist_values)

# Columns Summary

st.subheader('| QUICK SUMMARY')

col2, col3 = st.columns(2)
# column 2 - Count of clients
with col2:
    st.title(df.SK_ID_CURR.count())
    st.text('Clients')
# column 3 - Sum of clients
with col3:
    st.title(df.size.sum())
    st.text('CLIENTS')

