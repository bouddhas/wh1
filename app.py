from flask import Flask, render_template, jsonify, request
import json
import requests
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))



@app.route('/api',methods=['POST'])
def predict():
    

    data = request.get_json(force=True)
    data = json.loads(data)
    print(data.values())
    new_lis = list(data.values())
    print('new_lis ok')
    result = np.array(new_lis)
    lis = list(data)
    colonnes = np.array(lis)
    new_df = pd.DataFrame([result],columns =colonnes)
    #new_result = result[1:]

    print(len(result))
    #print(len(new_result))
    #print(new_result)
    print(result)
    print ('results ok')

   
    
    prediction = model.predict(new_df)
    print('predict ok')
    pred = prediction[0]
    print(pred)
    return jsonify(int(pred))




if __name__ == "__main__":
    app.run(debug=True)
    
    