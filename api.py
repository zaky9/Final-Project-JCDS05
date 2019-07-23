from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

df = pd.read_csv('student_grade.csv')
model = joblib.load('model_ml')

# home route
@app.route('/')
def home():
    return render_template('home.html')

# result page
@app.route('/result', methods = ['POST'])
def result():
    
    Medu = request.form['Medu'] # one hot
    Fedu = request.form['Fedu'] # one hot
    Mjob = request.form['Mjob'] # one hot
    higher = request.form['higher'] # Boolean (0-1)
    studytime = request.form['studytime'] # Label Encoder (1-4)
    address = request.form['address']
    failures = int(request.form['failures']) # integers
    Dalc = request.form['Dalc'] # Label Encoder (1-5)
    absences = int(request.form['absences']) # integers
    traveltime = request.form['traveltime'] # Label Encoder (1-4)

    if Medu == 'M0':
        M0 = 1
        M1 = 0
        M2 = 0
        M3 = 0
        M4 = 0
    elif Medu == 'M1':
        M0 = 0
        M1 = 1
        M2 = 0
        M3 = 0
        M4 = 0
    elif Medu == 'M2':
        M0 = 0
        M1 = 0
        M2 = 1
        M3 = 0
        M4 = 0
    elif Medu == 'M3':
        M0 = 0
        M1 = 0
        M2 = 0
        M3 = 1
        M4 = 0
    else:
        M0 = 0
        M1 = 0
        M2 = 0
        M3 = 0
        M4 = 1
    
    if Fedu == 'F0':
        F0 = 1
        F1 = 0
        F2 = 0
        F3 = 0
        F4 = 0
    elif Fedu == 'F1':
        F0 = 0
        F1 = 1
        F2 = 0
        F3 = 0
        F4 = 0
    elif Fedu == 'F2':
        F0 = 0
        F1 = 0
        F2 = 1
        F3 = 0
        F4 = 0
    elif Fedu == 'F3':
        F0 = 0
        F1 = 0
        F2 = 0
        F3 = 1
        F4 = 0
    else:
        F0 = 0
        F1 = 0
        F2 = 0
        F3 = 0
        F4 = 1
    
    if Mjob == 'teacher':
        teacher = 1
        health = 0
        services = 0
        at_home = 0
        other = 0
    elif Mjob == 'health':
        teacher = 0
        health = 1
        services = 0
        at_home = 0
        other = 0
    elif Mjob == 'services':
        teacher = 0
        health = 0
        services = 1
        at_home = 0 
        other = 0
    elif Mjob == 'at_home':
        teacher = 0
        health = 0
        services = 0
        at_home = 1
        other = 0
    else:
        teacher = 0
        health = 0
        services = 0
        at_home = 0
        other = 1


    data=[M0,M1,M2,M3,M4,F0,F1,F2,F3,F4,teacher,health,services,at_home,other,higher,studytime,address,failures,Dalc,absences,traveltime]
    prediction = model.predict([data])[0]
    
    if int(prediction) == 1:
        conclusion = 'PASS'
    else:
        conclusion = 'FAILED'

    if Medu == 'M0':
        Medu = 'No education'
    elif Medu == 'M1':
        Medu = 'Primary education'
    elif Medu == 'M2':
        Medu = 'Middle Secondary education'
    elif Medu == 'M3':
        Medu = 'Secondary education'
    else:
        Medu = 'Higher education'

    if Fedu == 'F0':
        Fedu = 'No education'
    elif Fedu == 'F1':
        Fedu = 'Primary education'
    elif Fedu == 'F2':
        Fedu = 'Middle Secondary education'
    elif Fedu == 'F3':
        Fedu = 'Secondary education'
    else:
        Fedu = 'Higher education'

    if Mjob == "0":
        Mjob = 'Teacher'
    elif Mjob == "1":
        Mjob = 'Health Sector'
    elif Mjob == "2":
        Mjob = 'Services'
    elif Mjob == "3":
        Mjob = 'at home'
    else:
        Mjob = 'others'

    if int(higher) == 0:
        higher = 'No'
    else:
        higher = 'Yes'

    if studytime == "1":
        studytime = 'Less than 2 hour'
    elif studytime == "2":
        studytime = '2 to 5 hours'
    elif studytime == "3":
        studytime = '5 to 10 hours'
    else:
        studytime = 'more than 10 hours'
    
    if address == "0":
        address = 'Rural area'
    else:
        address = 'Urban area'
    
    if Dalc == "1":
        Dalc = 'very rare'
    elif Dalc == "2":
        Dalc = 'Once in a while'
    elif Dalc == "3":
        Dalc = 'Occasionally'
    elif Dalc == "4":
        Dalc = 'Frequently'
    else:
        Dalc = 'Daily'

    if traveltime == "1":
        traveltime = "less than 15 mins"
    elif traveltime == "2":
        traveltime = "15 to 30 mins"
    elif traveltime == "2":
        traveltime = "30 mins to 1 hour"
    else:
        traveltime = "More than 1 hour"
    

    datahasil = {
        'Medu': Medu,
        'Fedu': Fedu,
        'MJob' : Mjob,
        'higher': higher,
        'studytime': studytime,
        'address' : address,
        'failures' : failures,
        'Dalc': Dalc,
        'absences' : absences,
        'traveltime': traveltime,
        'prediction': prediction,
        'conclusion': conclusion
    }
    print(conclusion)
    return render_template('result.html', result=datahasil)
      
# Activate server
if __name__ == '__main__':
    model = joblib.load('model_ml')
    app.run(debug = True, port = 5000)