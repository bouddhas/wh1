import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('OC credit default project')
df = pd.read_csv("data.csv")

add_selectbox = st.sidebar.selectbox(
    "What would you like to see?",
    ("full clients", "one client")
)

if 'full clients' in add_selectbox : # If user selects full clients  
    df["AGE"] = df['DAYS_BIRTH']/365
    st.subheader('Distribution of Age')
    fig, ax = plt.subplots()
    df.hist(
        bins=20,
        column="AGE",
        grid=False,
        figsize=(5, 5),
        color="#86bf91",
        zorder=2,
        rwidth=0.9,
        ax=ax,)
    st.write(fig)

# Add some matplotlib code !
    df["Years_employed"] = df['DAYS_EMPLOYED']/365*-1

    fig, ax = plt.subplots()
    df.hist(
        bins=20,
        column="Years_employed",
        grid=False,
        figsize=(5, 5),
        color="#86bf91",
        zorder=2,
        rwidth=0.9,
        ax=ax,)
    st.write(fig)
  
    fig, ax = plt.subplots()
    df.hist(
        bins=100,
        column="AMT_CREDIT",
        grid=False,
        figsize=(5, 5),
        color="#86bf91",
        zorder=2,
        rwidth=0.9,
        ax=ax,)
    st.write(fig)

# Columns Summary

    st.subheader('| QUICK SUMMARY')


    col1, col2, col3, col4 = st.columns(4)
# column 1 - Count of clients phones
    with col1:
        st.title(df.FLAG_PHONE.sum())
        st.text('Clients owning phone')

    # column 2 - Count of female clients
    with col2:
        st.title(df.CODE_GENDER_F.sum())
        st.text('Female Clients')
# column 3 - Sum of clients
    with col3:
        st.title(df.SK_ID_CURR.count())
        st.text('CLIENTS')
# column 4 - Sum of clients that have car
    with col4:
        st.title(df.FLAG_OWN_CAR.sum())
        st.text('Clients owning car')

    st.title("Streamlit Double Sliders")

    st.subheader("Slider")
    slider_range = st.slider("Double ended slider", value=[15,75])

    st.info("Our slider range has type: %s" %type(slider_range))
    st.write("Slider range:", slider_range, slider_range[0], slider_range[1])

else : 
    st.subheader("Insight of a client")
    add_selectbox_2 = st.selectbox(
    "Choose a client",
    df.SK_ID_CURR
)



