from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

test=pd.read_csv("test_data.csv",error_bad_lines=False)
x_test=test.drop('prognosis',axis=1)

@app.route('/')
def about():
    default = ['', '', '', '', '', '']
    return render_template("index.html", form_values = default)

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        col=x_test.columns
        inputt = [str(x) for x in request.form.values()]

        print(inputt)
        b=[0]*132
        for x in range(0,132):
            for y in inputt:
                if(col[x]==y):
                    b[x]=1
        b=np.array(b)
        b=b.reshape(1,132)
        prediction = model.predict(b)
        prediction=prediction[0]
    return render_template('index.html', pred="The disease predicted for these symptoms is {}.".format(prediction), form_values = inputt)
    

if __name__ == '__main__':
  app.run(debug = True)

