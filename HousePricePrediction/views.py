import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np

def home(request):
    return render(request,'home.html')

def predict(request):
    return render(request,'predict.html')

def result(request):
    if request.method == 'POST':
        try:
            data = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                       'HPPre', 'USA_Housing.csv'))
            data = data.drop(['Address'], axis=1)

            x = data.drop(['Price'], axis=1)
            y = data['Price']

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.30)

            model = LinearRegression()
            model.fit(x_train, y_train)

            var1 = float(request.POST['n1'])
            var2 = float(request.POST['n2'])
            var3 = float(request.POST['n3'])
            var4 = float(request.POST['n4'])
            var5 = float(request.POST['n5'])

            prediction = model.predict(np.array([var1, var2, var3, var4, var5]).reshape(1, 5))
            result = round(prediction[0])
            price = "The predicted price of the house is: $" + str(result)
            return render(request, 'predict.html', {'result': price})
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'predict.html', {'result': error_message})
    return render(request, 'predict.html')