from http import client
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from flask import Flask, request, jsonify
import xgboost
import streamlit.components.v1 as components
import seaborn as sn 
import sklearn
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import tkinter
import pickle
import pylab as pl
import json
import requests


st.title('OC credit default project')
df = pd.read_csv("new_data.csv")

shap.initjs()
#@st.cache
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

model = pickle.load(open("finalized_model.sav", 'rb'))


add_selectbox = st.sidebar.selectbox(
    "What would you like to see?",
    ("full clients", "one client")
)

if 'full clients' in add_selectbox : # If user selects full clients  

    st.subheader('Overview of data')
    st.dataframe(df)

    df["AGE"] = df['DAYS_BIRTH']/365
    df['AGE'] = df['AGE'].astype(int)
    conditions = [
        (df['CODE_GENDER_F'] == 1),
        (df['CODE_GENDER_F'] == 0)]
    values = ['F', 'M']
    

    df['SEX'] = np.select(conditions, values)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader('Boxplot of Age by sex')
    st.write(sn.boxplot(x='SEX', y='AGE', data=df[['SEX', 'AGE']]))
    st.pyplot()

    st.subheader('Distribution of Age')
    df2 = df[['AGE', 'SEX']]
    df3 = df2.groupby(by =['AGE', 'SEX'])['AGE'].count().unstack()
    df4 = df3.reset_index()
    M = df4['M'].values.tolist()
    F = df4['F'].values.tolist()
    A = df4['AGE'].values.tolist()
    test = pd.DataFrame(list(zip(M, F, A)),
                columns =['M', 'F', 'A'])
    test2 = test.set_index([A])
    test2 = test2.drop(columns = ['A'])
    st.bar_chart(test2)


# Add hist years employed
    df["Years_employed"] = df['DAYS_EMPLOYED']/365*-1
    st.subheader('Distribution of years employed')
    df2 = df[['Years_employed', 'SEX']]
    df2 = df2.dropna()
    df2['Years_employed'] = df2['Years_employed'].astype(int)
    df3 = df2.groupby(by =['Years_employed', 'SEX'])['Years_employed'].count().unstack()
    df4 = df3.reset_index()
    M = df4['M'].values.tolist()
    F = df4['F'].values.tolist()
    A = df4['Years_employed'].values.tolist()
    test = pd.DataFrame(list(zip(M, F, A)),
               columns =['M', 'F', 'A'])
    test2 = test.set_index([A])
    test2 = test2.drop(columns = ['A'])
    test2 = test2.dropna()
    st.bar_chart(test2)
    
    
    st.subheader('Distribution of Income amount')
    fig, ax = plt.subplots()
    df.hist(
        bins=1000,
        column="AMT_INCOME_TOTAL",	
        grid=False,
        figsize=(5, 5),
        zorder=2,
        rwidth=0.9,
        ax=ax,)
    ax.ticklabel_format(style='plain', useOffset=False)
    plt.xlim([0, 1600000])
    st.write(fig)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)


# Columns Summary

    st.subheader('| QUICK SUMMARY')


    col2, col3, col4 = st.columns(3)
    # column 2 - Count of female clients
    with col2:
        st.title(df.CODE_GENDER_F.sum())
        st.text('Female Clients')
# column 3 - Sum of clients
    with col3:
        st.title(df.SK_ID_CURR.count())
        st.text('Clients')
# column 4 - Sum of clients that have car
    with col4:
        st.title(df.FLAG_OWN_CAR.sum())
        st.text('Clients owning car')

    col5, col6 = st.columns(2)
# column 5 - Count of clients credit amount
    with col5:
        mean = int(round(df['AMT_CREDIT'].median())) 
        st.title(mean)
        st.text('Median amount of loan')
# column 6 - Count of clients credit amount
    with col6:
        mean = int(round(df['AMT_INCOME_TOTAL'].median())) 
        st.title(mean)
        st.text('Median amount of income')


    
else : 
    st.subheader("Insight of a client")
    add_selectbox_2 = st.selectbox(
    "Choose a client",
    df.SK_ID_CURR)

    client_choice = df.loc[(df['SK_ID_CURR'] == add_selectbox_2)]
    print(client_choice)
                
    if st.button('Get predictions ?'):
                    
        # requête de  l'API :
            
        url = 'http://127.0.0.1:5000/api'
        print(client_choice.iloc[0])
        r = requests.post(url,json=(client_choice.iloc[0].to_json()))
        print('ok')
        print(r)
        prediction = r.json()
        print(prediction)
                                
        if prediction == 0:
            st.success('Féliciations, votre crédit est accordé !')
        if prediction == 1:
            st.error("Nous sommes désolés, votre crédit n'est pas accordé.")


    

    # caractéristiques client :
    amt_credit_client = df[df['SK_ID_CURR']== add_selectbox_2]['AMT_CREDIT'].values
    amt_income_client = df[df['SK_ID_CURR']== add_selectbox_2]['AMT_INCOME_TOTAL'].values

    
    shap_client = df.loc[df['SK_ID_CURR']== add_selectbox_2]

     # Affichage des graphes :
    st.subheader("Clients characteristics")
    pl.subplot(2, 1, 1)                
    ax1 = sn.displot(df['AMT_CREDIT'])
    plt.xlim([0, 2500000])
    plt.ticklabel_format(style='plain', useOffset=False)
    plt.axvline(amt_credit_client, color='red')
    st.pyplot(pl) 
                
    pl.subplot(2, 1, 2)
    ax2 = sn.displot(df['AMT_INCOME_TOTAL'])
    plt.xlim([0, 1000000])
    plt.ticklabel_format(style='plain', useOffset=False)
    plt.axvline(amt_income_client, color='red')
                
    pl.tight_layout()
    st.pyplot(pl) 

    st.subheader("Local importance")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(shap_client)
    st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], df.iloc[0,:]))

    st.subheader("Most important features for decision")
    fig, ax = plt.subplots(nrows=1, ncols=1)
    shap.summary_plot(shap_values, df, plot_type='bar')
    st.pyplot(fig)



    #if __name__ == "__main__":
        #app.run(debug=True)
